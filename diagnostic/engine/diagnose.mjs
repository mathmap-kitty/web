const CORE_ABILITIES = ['CONCEPT', 'RECOGNITION', 'APPLICATION'];
const REQUIRED_ATTEMPT_FIELDS = ['sessionId','learningCycleId','itemId','itemVersion','attemptOrdinal','primaryConceptId','ability','correct','hintUsed','submittedAt'];
const SCORE_WEIGHTS = { A: 0.55, T: 0.15, S: 0.10, R: 0.20 };

function ratio(correct, total) { return total ? correct / total : null; }
function hasRequiredFields(attempt) {
  return REQUIRED_ATTEMPT_FIELDS.every(field => attempt[field] !== undefined && attempt[field] !== null);
}
function byTime(a, b) {
  return String(a.submittedAt).localeCompare(String(b.submittedAt)) || a.attemptOrdinal - b.attemptOrdinal;
}
function weightedScore(dimensions) {
  let numerator = 0, denominator = 0;
  for (const [key, weight] of Object.entries(SCORE_WEIGHTS)) {
    if (dimensions[key] === null) continue;
    numerator += dimensions[key] * weight;
    denominator += weight;
  }
  return denominator ? numerator / denominator : null;
}

export function evaluateConcept(input) {
  const flags = new Set();
  const excludedEvidence = [];
  const questionMap = new Map((input.questions ?? []).map(q => [q.itemId, q]));
  const raw = [...(input.attempts ?? [])].sort(byTime);
  const currentLearningCycleId = input.currentLearningCycleId ?? raw[0]?.learningCycleId ?? null;

  const eligible = [];
  for (const attempt of raw) {
    if (!hasRequiredFields(attempt)) {
      excludedEvidence.push({ attemptId: attempt.attemptId ?? attempt.itemId ?? 'unknown', reason: 'INVALID' });
      continue;
    }
    if (attempt.learningCycleId !== currentLearningCycleId) {
      flags.add('OTHER_LEARNING_CYCLE_EXCLUDED');
      excludedEvidence.push({ attemptId: attempt.attemptId ?? attempt.itemId, reason: 'OTHER_LEARNING_CYCLE' });
      continue;
    }
    const publication = questionMap.get(attempt.itemId)?.publicationStatus ?? attempt.itemPublicationStatus ?? 'APPROVED_PUBLISHED';
    if (publication !== 'APPROVED_PUBLISHED') {
      flags.add('UNPUBLISHED_ITEM_EXCLUDED');
      excludedEvidence.push({ attemptId: attempt.attemptId ?? attempt.itemId, reason: 'UNPUBLISHED_ITEM' });
      continue;
    }
    eligible.push(attempt);
  }

  const dedupe = new Set(), deduplicated = [];
  for (const attempt of eligible) {
    const key = `${attempt.sessionId}:${attempt.itemId}:${attempt.itemVersion}:${attempt.attemptOrdinal}`;
    if (dedupe.has(key)) {
      flags.add('DUPLICATE_IGNORED');
      excludedEvidence.push({ attemptId: attempt.attemptId ?? attempt.itemId, reason: 'DUPLICATE' });
      continue;
    }
    dedupe.add(key);
    deduplicated.push(attempt);
  }

  const firstByItem = new Map();
  for (const attempt of deduplicated) {
    if (!firstByItem.has(attempt.itemId)) firstByItem.set(attempt.itemId, attempt);
    else excludedEvidence.push({ attemptId: attempt.attemptId ?? attempt.itemId, reason: 'NOT_FIRST_GRADED' });
  }
  const independent = [...firstByItem.values()];
  if (deduplicated.length !== independent.length) flags.add('NONINDEPENDENT_ITEM_VERSION');
  if (deduplicated.some(a => a.timeRatio === null)) flags.add('TIME_DATA_MISSING');
  if (deduplicated.some(a => a.confidence === null)) flags.add('CONFIDENCE_DATA_MISSING');

  const decision = independent.filter(a => !a.hintUsed && !Number.isInteger(a.delayedDay) && a.source !== 'IMMEDIATE_VARIANT');
  const immediateAll = independent.filter(a => a.source === 'IMMEDIATE_VARIANT');
  const immediate = input.currentRemediationCycleId
    ? immediateAll.filter(a => a.remediationCycleId === input.currentRemediationCycleId)
    : immediateAll;
  const delayedAll = independent.filter(a => Number.isInteger(a.delayedDay));
  const delayed = input.currentRemediationCycleId
    ? delayedAll.filter(a => a.remediationCycleId === input.currentRemediationCycleId)
    : delayedAll;
  const historicalDelayed = input.currentRemediationCycleId
    ? delayedAll.filter(a => a.remediationCycleId !== input.currentRemediationCycleId)
    : [];
  if (delayed.some(a => !a.correct)) flags.add('RETEST_FAILED');
  if (historicalDelayed.some(a => !a.correct)) flags.add('HISTORICAL_RETEST_FAILURE');
  if (decision.filter(a => a.correct && Number(a.timeRatio) > 1.5).length >= 2) flags.add('SPEED_SUPPORT');

  const decisionAbilities = new Set(decision.map(a => a.ability));
  if (CORE_ABILITIES.some(ability => independent.some(a => a.ability === ability && a.hintUsed) && !decisionAbilities.has(ability))) flags.add('HINT_DEPENDENT');

  const risks = new Map();
  for (const attempt of independent) {
    if (!attempt.hintUsed && attempt.correct === false && attempt.confidence === 'HIGH') {
      const prior = risks.get(attempt.ability);
      risks.set(attempt.ability, { state:'OPEN', wrongItems:new Set([...(prior?.wrongItems ?? []),attempt.itemId]), confirmingItems:new Set(), hasDelayedConfirmation:false });
      continue;
    }
    const risk = risks.get(attempt.ability);
    if (!risk || risk.state === 'RESOLVED' || attempt.hintUsed || risk.wrongItems.has(attempt.itemId)) continue;
    if (!attempt.correct) {
      risk.state='OPEN'; risk.confirmingItems.clear(); risk.hasDelayedConfirmation=false; continue;
    }
    risk.confirmingItems.add(attempt.itemId);
    if (Number.isInteger(attempt.delayedDay) && attempt.delayedDay >= 1) risk.hasDelayedConfirmation=true;
    risk.state = risk.confirmingItems.size >= 2 && risk.hasDelayedConfirmation ? 'RESOLVED' : 'CONFIRMING';
  }
  const riskStates=[...risks.values()].map(r=>r.state);
  const riskState=riskStates.includes('OPEN')?'OPEN':riskStates.includes('CONFIRMING')?'CONFIRMING':riskStates.includes('RESOLVED')?'RESOLVED':null;
  if(riskStates.length) flags.add('HISTORICAL_HIGH_CONFIDENCE_WRONG');
  if(riskStates.some(s=>s!=='RESOLVED')) flags.add('HIGH_CONFIDENCE_WRONG');

  const weakAbilities=CORE_ABILITIES.filter(ability=>{
    const group=decision.filter(a=>a.ability===ability);
    return group.length && ratio(group.filter(a=>a.correct).length,group.length)<2/3;
  });
  const missingIndependentAbilities=CORE_ABILITIES.filter(a=>!decisionAbilities.has(a));
  const overallAccuracy=ratio(decision.filter(a=>a.correct).length,decision.length);
  const immediatePassedAbilities=new Set(immediate.filter(a=>!a.hintUsed&&a.correct).map(a=>a.ability));
  const immediateComplete=weakAbilities.every(ability=>immediatePassedAbilities.has(ability));
  const delayedAbilities=new Set(delayed.map(a=>a.ability));
  const requiredDelayedAbilities=weakAbilities.length===3?3:2;
  const stable=immediateComplete && delayed.length>=requiredDelayedAbilities && delayed.some(a=>a.delayedDay>=3) && delayedAbilities.size>=requiredDelayedAbilities && delayed.every(a=>a.correct) && riskStates.every(s=>s==='RESOLVED');

  let status;
  if(!decision.length && input.legacyEvidence){ status='UNTESTED'; flags.add('LEGACY_AUXILIARY_ONLY'); }
  else if(!decision.length) status='UNTESTED';
  else if(decision.length<3 || missingIndependentAbilities.length) status='INSUFFICIENT_EVIDENCE';
  else {
    status=stable?'STABLE':overallAccuracy<2/3 || weakAbilities.length?'NEEDS_REVIEW':'EMERGING';
    if(immediate.length&&!immediateComplete) flags.add('IMMEDIATE_VARIANT_FAILED');
    if(weakAbilities.length&&!immediate.length) flags.add('IMMEDIATE_VARIANT_REQUIRED');
    if(immediateComplete&&immediate.length) flags.add('IMMEDIATE_VARIANT_PASSED');
    if(delayed.length&&!stable&&!flags.has('RETEST_FAILED')) flags.add('RETEST_INCOMPLETE');
  }

  const timed=decision.filter(a=>a.timeRatio!==null && Number.isFinite(Number(a.timeRatio)));
  const dimensions={
    A:overallAccuracy,
    T:ratio(decision.filter(a=>a.ability==='APPLICATION'&&a.correct).length,decision.filter(a=>a.ability==='APPLICATION').length),
    S:ratio(timed.filter(a=>a.correct&&Number(a.timeRatio)<=1.5).length,timed.length),
    R:ratio(delayed.filter(a=>a.correct).length,delayed.length)
  };
  return {
    status, score:weightedScore(dimensions), dimensions, flags:[...flags].sort(),
    validAttemptCount:deduplicated.length, independentItemCount:independent.length,
    accuracy:overallAccuracy, immediateAccuracy:ratio(immediate.filter(a=>a.correct).length,immediate.length), delayedAccuracy:dimensions.R, weakAbilities, immediateComplete, immediatePassedAbilities:[...immediatePassedAbilities], missingIndependentAbilities,
    riskState, excludedEvidence, currentLearningCycleId
  };
}

export function diagnose(input) {
  const conceptIds=input.conceptIds ?? [...new Set((input.attempts ?? []).map(a=>a.primaryConceptId))];
  return {
    algorithmVersion:'1.1.0', generatedAt:input.asOf,
    learningCycleId:input.currentLearningCycleId,
    masteryRecords:conceptIds.map(kpId=>({ kpId, ...evaluateConcept({ ...input, attempts:(input.attempts??[]).filter(a=>a.primaryConceptId===kpId) }) }))
  };
}
