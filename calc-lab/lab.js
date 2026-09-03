/* ============================================================
   lab.js — 選修數學甲（上）互動教具 共用程式
   內容：① 運算式解析（自訂函數）② 數值工具 ③ 畫布繪圖 ④ 共用 UI
   沒有任何外部相依；KaTeX 有載入就用，沒有就退回純文字。
   ============================================================ */
(function (global) {
  "use strict";
  var Lab = {};

  /* ----------------------------------------------------------
     ① 運算式解析：把 "x^2-2x+3" 變成 JS 函數＋TeX 字串
     支援：+ - * / ^ ( )、隱含乘法（2x、x(4-x)）、² ³、π、√
           sin cos tan sqrt abs exp ln log、常數 pi e、變數 x（t 同義）
     ---------------------------------------------------------- */
  var FN = {
    sin: Math.sin, cos: Math.cos, tan: Math.tan, sqrt: Math.sqrt,
    abs: Math.abs, exp: Math.exp, ln: Math.log,
    log: function (v) { return Math.log(v) / Math.LN10; }
  };
  var FN_NAMES = ["sqrt", "sin", "cos", "tan", "abs", "exp", "ln", "log"];
  var CONST = { pi: Math.PI, e: Math.E };

  function tokenize(src) {
    var s = String(src)
      .replace(/\s+/g, "")
      .replace(/[×·]/g, "*").replace(/÷/g, "/").replace(/[−–]/g, "-")
      .replace(/π/g, "pi").replace(/√/g, "sqrt")
      .replace(/²/g, "^2").replace(/³/g, "^3").replace(/⁴/g, "^4")
      .replace(/＾/g, "^").replace(/（/g, "(").replace(/）/g, ")");
    if (!s) throw new Error("請輸入函數");
    var toks = [], i = 0, m, c;
    while (i < s.length) {
      c = s[i];
      if (/[0-9.]/.test(c)) {
        m = s.slice(i).match(/^(\d+\.?\d*|\.\d+)/);
        toks.push({ t: "num", v: parseFloat(m[0]) }); i += m[0].length; continue;
      }
      if (/[a-zA-Z]/.test(c)) {
        m = s.slice(i).match(/^[a-zA-Z]+/)[0]; i += m.length;
        /* 一串字母可能是 "xsinx"：從頭貪婪切成 函數／常數／變數 */
        var rest = m, hit;
        while (rest.length) {
          hit = null;
          for (var k = 0; k < FN_NAMES.length; k++) {
            if (rest.indexOf(FN_NAMES[k]) === 0) { hit = { t: "fn", v: FN_NAMES[k] }; break; }
          }
          if (!hit && rest.indexOf("pi") === 0) hit = { t: "const", v: "pi" };
          if (!hit && (rest[0] === "x" || rest[0] === "t")) hit = { t: "var", v: rest[0] };
          if (!hit && rest[0] === "e") hit = { t: "const", v: "e" };
          if (!hit) throw new Error("不認識的名稱「" + rest + "」");
          toks.push(hit); rest = rest.slice(hit.v.length);
        }
        continue;
      }
      if ("+-*/^()".indexOf(c) >= 0) { toks.push({ t: c }); i++; continue; }
      throw new Error("看不懂的符號「" + c + "」");
    }
    /* 隱含乘法：值的結尾 接 值的開頭 → 補 * */
    var out = [], prev = null;
    for (i = 0; i < toks.length; i++) {
      var cur = toks[i];
      if (prev) {
        var endsVal = (prev.t === "num" || prev.t === "var" || prev.t === "const" || prev.t === ")");
        var startsVal = (cur.t === "num" || cur.t === "var" || cur.t === "const" || cur.t === "fn" || cur.t === "(");
        if (endsVal && startsVal) out.push({ t: "*" });
      }
      out.push(cur); prev = cur;
    }
    return out;
  }

  function parse(src) {
    var toks = tokenize(src), pos = 0;
    function peek() { return toks[pos]; }
    function eat(t) {
      var k = toks[pos];
      if (!k || k.t !== t) throw new Error(t === ")" ? "括號沒有配對" : "算式不完整");
      pos++; return k;
    }
    function expr() {
      var n = term();
      while (peek() && (peek().t === "+" || peek().t === "-")) {
        var op = toks[pos++].t; n = { k: "bin", op: op, l: n, r: term() };
      }
      return n;
    }
    function term() {
      var n = unary();
      while (peek() && (peek().t === "*" || peek().t === "/")) {
        var op = toks[pos++].t; n = { k: "bin", op: op, l: n, r: unary() };
      }
      return n;
    }
    function unary() {
      if (peek() && peek().t === "-") { pos++; return { k: "neg", a: unary() }; }
      if (peek() && peek().t === "+") { pos++; return unary(); }
      return power();
    }
    function power() {
      var b = atom();
      if (peek() && peek().t === "^") { pos++; return { k: "bin", op: "^", l: b, r: unary() }; }
      return b;
    }
    function atom() {
      var k = peek();
      if (!k) throw new Error("算式不完整");
      if (k.t === "num") { pos++; return { k: "num", v: k.v }; }
      if (k.t === "var") { pos++; return { k: "var" }; }
      if (k.t === "const") { pos++; return { k: "const", v: k.v }; }
      if (k.t === "fn") {
        pos++;
        var arg;
        if (peek() && peek().t === "(") { pos++; arg = expr(); eat(")"); }
        else arg = power();               /* sinx、sqrt x 這種寫法 */
        return { k: "fn", f: k.v, arg: arg };
      }
      if (k.t === "(") { pos++; var n = expr(); eat(")"); return n; }
      throw new Error("「" + k.t + "」放的位置不對");
    }
    var ast = expr();
    if (pos < toks.length) throw new Error("多出來的「" + toks[pos].t + "」");
    return ast;
  }

  function compile(n) {
    var a, b, g, v;
    switch (n.k) {
      case "num": v = n.v; return function () { return v; };
      case "var": return function (x) { return x; };
      case "const": v = CONST[n.v]; return function () { return v; };
      case "neg": a = compile(n.a); return function (x) { return -a(x); };
      case "fn": g = FN[n.f]; a = compile(n.arg); return function (x) { return g(a(x)); };
      case "bin":
        a = compile(n.l); b = compile(n.r);
        switch (n.op) {
          case "+": return function (x) { return a(x) + b(x); };
          case "-": return function (x) { return a(x) - b(x); };
          case "*": return function (x) { return a(x) * b(x); };
          case "/": return function (x) { return a(x) / b(x); };
          case "^": return function (x) { return Math.pow(a(x), b(x)); };
        }
    }
    throw new Error("內部錯誤");
  }

  function numTex(v) {
    if (Number.isInteger(v)) return String(v);
    return String(parseFloat(v.toPrecision(6)));
  }
  var PREC = { "+": 1, "-": 1, "*": 2, "/": 2, "^": 4 };
  function prec(n) {
    if (n.k === "bin") return n.op === "/" ? 5 : PREC[n.op];
    if (n.k === "neg") return 3;
    return 6;
  }
  function wrap(s) { return "\\left(" + s + "\\right)"; }
  function tex(n, varName) {
    var l, r;
    switch (n.k) {
      case "num": return numTex(n.v);
      case "var": return varName;
      case "const": return n.v === "pi" ? "\\pi " : "e";
      case "neg":
        l = tex(n.a, varName);
        return "-" + (prec(n.a) < 3 ? wrap(l) : l);
      case "fn":
        l = tex(n.arg, varName);
        if (n.f === "sqrt") return "\\sqrt{" + l + "}";
        if (n.f === "abs") return "\\left|" + l + "\\right|";
        if (n.arg.k === "var" || n.arg.k === "num" || n.arg.k === "const") return "\\" + n.f + " " + l;
        return "\\" + n.f + wrap(l);
      case "bin":
        l = tex(n.l, varName); r = tex(n.r, varName);
        if (n.op === "/") return "\\frac{" + l + "}{" + r + "}";
        if (n.op === "^") {
          var base = (n.l.k === "num" || n.l.k === "var" || n.l.k === "const") ? l : wrap(l);
          return base + "^{" + r + "}";
        }
        if (n.op === "*") {
          if (prec(n.l) < 2) l = wrap(l);
          var rWrapped = (prec(n.r) < 2 || n.r.k === "neg");
          if (rWrapped) r = wrap(r);
          /* 2·3 要點乘，2x 直接並排；右邊以數字開頭（且沒被括號包住）也要點乘 */
          var rStartsNum = !rWrapped && ((n.r.k === "num") ||
            (n.r.k === "bin" && n.r.op !== "/" && leftmost(n.r).k === "num"));
          return l + (rStartsNum ? "\\cdot " : "") + r;
        }
        if (prec(n.r) <= 1 || (n.op === "-" && n.r.k === "neg")) r = wrap(r);
        return l + (n.op === "+" ? "+" : "-") + r;
    }
    return "?";
  }
  function leftmost(n) { while (n.k === "bin" && n.op !== "/") n = n.l; return n; }

  /** Lab.parseFn("x^2-2x") → {f, tex, src}；失敗會 throw Error（訊息可直接顯示） */
  Lab.parseFn = function (src, varName) {
    var ast = parse(src), f = compile(ast);
    var probe = f(0.37);
    if (typeof probe !== "number") throw new Error("算不出數值");
    return { f: f, tex: tex(ast, varName || "x"), src: String(src).trim() };
  };
  /** Lab.parseNum("pi/2") → 1.5707…；區間端點用 */
  Lab.parseNum = function (src) {
    var v = compile(parse(src))(0);
    if (!isFinite(v)) throw new Error("「" + src + "」不是數");
    return v;
  };

  /* ----------------------------------------------------------
     ② 數值工具
     ---------------------------------------------------------- */
  Lab.simpson = function (f, a, b, n) {
    n = n || 2000; if (n % 2) n++;
    var h = (b - a) / n, s = f(a) + f(b), i;
    for (i = 1; i < n; i++) s += f(a + i * h) * (i % 2 ? 4 : 2);
    return s * h / 3;
  };
  Lab.deriv = function (f, x, h) {
    h = h || 1e-5; return (f(x + h) - f(x - h)) / (2 * h);
  };
  /** 小段 [x0,x1] 上的最小值與最大值（取樣） */
  Lab.extremes = function (f, x0, x1, k) {
    k = k || 16;
    var mn = Infinity, mx = -Infinity, i, v;
    for (i = 0; i <= k; i++) {
      v = f(x0 + (x1 - x0) * i / k);
      if (v < mn) mn = v; if (v > mx) mx = v;
    }
    return [mn, mx];
  };
  Lab.range = function (f, a, b, k) {
    return Lab.extremes(f, a, b, k || 400);
  };
  Lab.fmt = function (v, d) {
    if (!isFinite(v)) return "—";
    d = (d === undefined) ? 5 : d;
    var s = Math.abs(v).toFixed(d);
    return (v < 0 && parseFloat(s) !== 0 ? "−" : "") + s;
  };
  Lab.short = function (v) {
    if (Math.abs(v) < 1e-9) return "0";
    return String(parseFloat(v.toFixed(3))).replace("-", "−");
  };
  Lab.niceStep = function (span, target) {
    var raw = span / (target || 5), p = Math.pow(10, Math.floor(Math.log(raw) / Math.LN10));
    var m = raw / p;
    return (m < 1.5 ? 1 : m < 3 ? 2 : m < 7 ? 5 : 10) * p;
  };

  /* ----------------------------------------------------------
     ③ 畫布：Retina 適配＋資料座標繪圖
     ---------------------------------------------------------- */
  Lab.pal = function () {
    var cs = getComputedStyle(document.documentElement);
    function g(n, d) { return (cs.getPropertyValue(n) || d).trim() || d; }
    return {
      maroon: g("--maroon", "#8c2740"), maroonD: g("--maroon-d", "#6f1f33"),
      teal: g("--teal", "#1f6f78"), amber: g("--amber", "#b45309"),
      ans: g("--ans", "#c0392b"), ink: g("--ink", "#2b2b2b"), mut: g("--mut", "#9a857c"),
      line: g("--line", "#e7dcd6"), page: g("--page", "#f7f2ee"), card: g("--card", "#ffffff"),
      rose: g("--rose", "#c96f88"), roseBg: g("--rose-bg", "#f6e7ec"), grid: g("--grid", "#efe6e1")
    };
  };
  Lab.rgba = function (hex, a) {
    var h = hex.replace("#", "");
    if (h.length === 3) h = h[0] + h[0] + h[1] + h[1] + h[2] + h[2];
    return "rgba(" + parseInt(h.slice(0, 2), 16) + "," + parseInt(h.slice(2, 4), 16) + "," +
      parseInt(h.slice(4, 6), 16) + "," + a + ")";
  };

  /** 把 canvas 撐滿父元素並處理 DPR；回傳 [w,h]（CSS 像素） */
  Lab.fit = function (canvas) {
    var box = canvas.parentElement.getBoundingClientRect();
    var dpr = window.devicePixelRatio || 1;
    var w = Math.max(240, Math.round(box.width)), h = Math.max(120, Math.round(box.height));
    canvas.width = Math.round(w * dpr); canvas.height = Math.round(h * dpr);
    canvas.style.width = w + "px"; canvas.style.height = h + "px";
    canvas.getContext("2d").setTransform(dpr, 0, 0, dpr, 0, 0);
    return [w, h];
  };

  /**
   * new Lab.Plot(ctx, box, xr, yr)
   *   box = {x,y,w,h, padL,padR,padT,padB}（CSS 像素）
   *   xr = [xlo,xhi], yr = [ylo,yhi]
   */
  Lab.Plot = function (ctx, box, xr, yr) {
    this.ctx = ctx; this.P = Lab.pal();
    this.x0 = box.x + (box.padL === undefined ? 48 : box.padL);
    this.y0 = box.y + (box.padT === undefined ? 16 : box.padT);
    this.w = box.w - (box.padL === undefined ? 48 : box.padL) - (box.padR === undefined ? 16 : box.padR);
    this.h = box.h - (box.padT === undefined ? 16 : box.padT) - (box.padB === undefined ? 34 : box.padB);
    this.xlo = xr[0]; this.xhi = xr[1]; this.ylo = yr[0]; this.yhi = yr[1];
    this.font = '"Microsoft JhengHei","PingFang TC","Noto Sans TC",system-ui,sans-serif';
  };
  Lab.Plot.prototype = {
    X: function (x) { return this.x0 + (x - this.xlo) / (this.xhi - this.xlo) * this.w; },
    Y: function (y) { return this.y0 + (this.yhi - y) / (this.yhi - this.ylo) * this.h; },
    clip: function () {
      this.ctx.save(); this.ctx.beginPath();
      this.ctx.rect(this.x0, this.y0, this.w, this.h); this.ctx.clip();
    },
    unclip: function () { this.ctx.restore(); },
    grid: function (opts) {
      opts = opts || {};
      var c = this.ctx, P = this.P, step = opts.step || Lab.niceStep(this.yhi - this.ylo, opts.lines || 5);
      var xstep = opts.xstep || Lab.niceStep(this.xhi - this.xlo, opts.xlines || 6);
      c.lineWidth = 1; c.strokeStyle = P.grid;
      c.font = "11.5px " + this.font; c.fillStyle = P.mut;
      var g;
      c.textAlign = "right"; c.textBaseline = "middle";
      for (g = Math.ceil(this.ylo / step) * step; g <= this.yhi + 1e-9; g += step) {
        c.beginPath(); c.moveTo(this.x0, this.Y(g) + 0.5); c.lineTo(this.x0 + this.w, this.Y(g) + 0.5); c.stroke();
        if (opts.ylabels !== false) c.fillText(Lab.short(g), this.x0 - 7, this.Y(g));
      }
      if (opts.xgrid !== false) {
        for (g = Math.ceil(this.xlo / xstep) * xstep; g <= this.xhi + 1e-9; g += xstep) {
          c.beginPath(); c.moveTo(this.X(g) + 0.5, this.y0); c.lineTo(this.X(g) + 0.5, this.y0 + this.h); c.stroke();
        }
      }
    },
    axes: function (opts) {
      opts = opts || {};
      var c = this.ctx, P = this.P;
      var ay = Math.min(Math.max(this.Y(0), this.y0), this.y0 + this.h);
      var ax = Math.min(Math.max(this.X(0), this.x0), this.x0 + this.w);
      c.strokeStyle = opts.color || P.ink; c.lineWidth = 1.3;
      c.beginPath(); c.moveTo(this.x0, ay); c.lineTo(this.x0 + this.w, ay); c.stroke();
      c.beginPath(); c.moveTo(ax, this.y0); c.lineTo(ax, this.y0 + this.h); c.stroke();
      c.font = "italic 13px " + this.font; c.fillStyle = P.ink;
      c.textAlign = "right"; c.textBaseline = "bottom";
      if (opts.xlabel !== false) c.fillText(opts.xlabel || "x", this.x0 + this.w - 2, ay - 4);
      c.textAlign = "left"; c.textBaseline = "top";
      if (opts.ylabel !== false) c.fillText(opts.ylabel || "y", ax + 6, this.y0 + 2);
    },
    tick: function (x, label, opts) {
      opts = opts || {};
      var c = this.ctx, P = this.P;
      var ay = Math.min(Math.max(this.Y(0), this.y0), this.y0 + this.h);
      c.strokeStyle = opts.color || P.ink; c.lineWidth = 1.2;
      c.beginPath(); c.moveTo(this.X(x), ay - 4); c.lineTo(this.X(x), ay + 4); c.stroke();
      c.font = (opts.bold ? "700 " : "") + "12.5px " + this.font;
      c.fillStyle = opts.color || P.ink; c.textAlign = "center"; c.textBaseline = "top";
      c.fillText(label, this.X(x), Math.min(ay + 6, this.y0 + this.h + 4));
    },
    curve: function (f, dom, opts) {
      opts = opts || {};
      var c = this.ctx, K = opts.samples || 500, i, x, y, on = false;
      var lo = dom ? dom[0] : this.xlo, hi = dom ? dom[1] : this.xhi;
      this.clip();
      c.strokeStyle = opts.color || this.P.maroon; c.lineWidth = opts.width || 2.4;
      c.lineJoin = "round"; c.lineCap = "round";
      c.setLineDash(opts.dash || []);
      c.globalAlpha = opts.alpha === undefined ? 1 : opts.alpha;
      c.beginPath();
      for (i = 0; i <= K; i++) {
        x = lo + (hi - lo) * i / K; y = f(x);
        if (!isFinite(y) || Math.abs(y) > 1e6) { on = false; continue; }
        var py = this.Y(y);
        if (py < this.y0 - 2000 || py > this.y0 + this.h + 2000) { on = false; continue; }
        if (!on) { c.moveTo(this.X(x), py); on = true; } else c.lineTo(this.X(x), py);
      }
      c.stroke(); c.setLineDash([]); c.globalAlpha = 1;
      this.unclip();
    },
    fillBetween: function (f, g, lo, hi, color, alpha) {
      var c = this.ctx, K = 300, i, x;
      this.clip();
      c.fillStyle = Lab.rgba(color, alpha === undefined ? 0.28 : alpha);
      c.beginPath();
      for (i = 0; i <= K; i++) { x = lo + (hi - lo) * i / K; c.lineTo(this.X(x), this.Y(f(x))); }
      for (i = K; i >= 0; i--) { x = lo + (hi - lo) * i / K; c.lineTo(this.X(x), this.Y(g(x))); }
      c.closePath(); c.fill();
      this.unclip();
    },
    rect: function (x0, x1, y0, y1, opts) {
      opts = opts || {};
      var c = this.ctx, X0 = this.X(x0), X1 = this.X(x1), Y0 = this.Y(y0), Y1 = this.Y(y1);
      var l = Math.min(X0, X1), t = Math.min(Y0, Y1), w = Math.abs(X1 - X0), h = Math.abs(Y1 - Y0);
      if (h < 0.5 || w < 0.3) return;
      this.clip();
      if (opts.fill) { c.fillStyle = Lab.rgba(opts.fill, opts.alpha === undefined ? 0.35 : opts.alpha); c.fillRect(l, t, w, h); }
      if (opts.stroke) {
        c.strokeStyle = Lab.rgba(opts.stroke, opts.strokeAlpha === undefined ? 0.9 : opts.strokeAlpha);
        c.lineWidth = opts.lineWidth || 1;
        c.strokeRect(l + 0.5, t + 0.5, Math.max(0, w - 1), Math.max(0, h - 1));
      }
      this.unclip();
    },
    line: function (xa, ya, xb, yb, opts) {
      opts = opts || {};
      var c = this.ctx;
      this.clip();
      c.strokeStyle = opts.color || this.P.ink; c.lineWidth = opts.width || 1.4;
      c.setLineDash(opts.dash || []);
      c.beginPath(); c.moveTo(this.X(xa), this.Y(ya)); c.lineTo(this.X(xb), this.Y(yb)); c.stroke();
      c.setLineDash([]);
      this.unclip();
    },
    /** 用斜率截距畫一整條直線（會自動裁在畫框內） */
    infLine: function (x1, y1, slope, opts) {
      this.line(this.xlo, y1 + slope * (this.xlo - x1), this.xhi, y1 + slope * (this.xhi - x1), opts);
    },
    dot: function (x, y, opts) {
      opts = opts || {};
      var c = this.ctx;
      c.fillStyle = opts.color || this.P.maroon;
      c.beginPath(); c.arc(this.X(x), this.Y(y), opts.r || 4.5, 0, Math.PI * 2); c.fill();
      if (opts.ring) { c.strokeStyle = "#fff"; c.lineWidth = 1.5; c.stroke(); }
    },
    text: function (x, y, str, opts) {
      opts = opts || {};
      var c = this.ctx;
      c.font = (opts.weight ? opts.weight + " " : "") + (opts.size || 13) + "px " + this.font;
      c.fillStyle = opts.color || this.P.ink;
      c.textAlign = opts.align || "left"; c.textBaseline = opts.base || "alphabetic";
      c.fillText(str, this.X(x) + (opts.dx || 0), this.Y(y) + (opts.dy || 0));
    },
    textPx: function (px, py, str, opts) {
      opts = opts || {};
      var c = this.ctx;
      c.font = (opts.weight ? opts.weight + " " : "") + (opts.size || 13) + "px " + this.font;
      c.fillStyle = opts.color || this.P.ink;
      c.textAlign = opts.align || "left"; c.textBaseline = opts.base || "top";
      c.fillText(str, px, py);
    }
  };

  /* ----------------------------------------------------------
     ④ 共用 UI
     ---------------------------------------------------------- */
  /** KaTeX 有就渲染，沒有就顯示純文字 */
  Lab.katex = function (el, texStr, display) {
    if (!el) return;
    if (global.katex) {
      try { global.katex.render(texStr, el, { displayMode: !!display, throwOnError: false }); return; }
      catch (e) { /* fall through */ }
    }
    el.textContent = texStr;
  };
  Lab.katexAll = function (root) {
    var nodes = (root || document).querySelectorAll("[data-tex]");
    Array.prototype.forEach.call(nodes, function (el) {
      Lab.katex(el, el.getAttribute("data-tex"), el.hasAttribute("data-display"));
    });
  };

  /** 膠囊選項列；回傳 {select(id)} 可用程式切換 */
  Lab.chips = function (host, items, currentId, onPick) {
    host.innerHTML = "";
    var btns = {};
    items.forEach(function (it) {
      var b = document.createElement("button");
      b.type = "button"; b.className = "chip";
      if (it.html) b.innerHTML = it.html; else b.textContent = it.btn || it.label;
      b.setAttribute("aria-pressed", String(it.id === currentId));
      b.addEventListener("click", function () { api.select(it.id); onPick(it); });
      host.appendChild(b); btns[it.id] = b;
    });
    var api = {
      select: function (id) {
        Object.keys(btns).forEach(function (k) { btns[k].setAttribute("aria-pressed", String(k === id)); });
      }
    };
    return api;
  };

  /**
   * 自訂函數輸入列
   * Lab.fnPanel(host, {varName:"x", interval:true, labels:{a:"a",b:"b"}, onApply:function(F){}})
   * F = {f, tex, src, a, b, custom:true}
   * 回傳 {fill(F)}：把預設函數填進欄位，學生可以直接改
   */
  Lab.fnPanel = function (host, opts) {
    opts = opts || {};
    var v = opts.varName || "x";
    var hasInt = opts.interval !== false;
    host.innerHTML =
      '<div class="fnrow">' +
      '  <label class="fnlab">f(' + v + ') =</label>' +
      '  <input class="fnin" type="text" spellcheck="false" autocomplete="off" aria-label="函數">' +
      '</div>' +
      '<div class="fnrow fnrow2">' +
      (hasInt ?
        '  <span class="fnlab">' + (opts.intLabel || "在") + '</span>' +
        '  <span class="fnint">[<input class="fna" type="text" aria-label="左端點">，' +
        '<input class="fnb" type="text" aria-label="右端點">]</span>' : "") +
      (opts.extra || "") +
      '  <button type="button" class="btn fnapply">套用</button>' +
      '</div>' +
      '<div class="fnerr" role="alert"></div>' +
      '<div class="fnhint">' + (opts.hint ||
        '可以用 <code>^</code> 次方、<code>sqrt</code>、<code>abs</code>、<code>sin</code> <code>cos</code>、<code>pi</code>；' +
        '例：<code>x^3-3x</code>、<code>4-x^2</code>、<code>sqrt(4-x^2)</code>、<code>abs(x-1)</code>') + '</div>';
    var inF = host.querySelector(".fnin"), inA = host.querySelector(".fna"), inB = host.querySelector(".fnb");
    var err = host.querySelector(".fnerr"), btn = host.querySelector(".fnapply");

    function apply() {
      err.textContent = "";
      try {
        var F = Lab.parseFn(inF.value, v);
        if (hasInt) {
          var a = Lab.parseNum(inA.value || "0"), b = Lab.parseNum(inB.value || "1");
          if (!(b > a)) throw new Error("右端點要比左端點大");
          F.a = a; F.b = b;
          var bad = 0, i, y;
          for (i = 0; i <= 200; i++) { y = F.f(a + (b - a) * i / 200); if (!isFinite(y)) bad++; }
          if (bad > 0) throw new Error("函數在這個區間裡有 " + bad + " 個點算不出來（除以 0 或根號裡是負數）");
        }
        F.custom = true;
        if (opts.onApply) opts.onApply(F);
      } catch (e) { err.textContent = "⚠ " + e.message; }
    }
    btn.addEventListener("click", apply);
    host.addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); apply(); } });
    return {
      fill: function (F) {
        inF.value = F.src || ""; err.textContent = "";
        if (hasInt) { inA.value = Lab.short(F.a); inB.value = Lab.short(F.b); }
      },
      apply: apply
    };
  };

  /**
   * 自動播放：Lab.player(btn, {tick:function(){return false 表示結束}, ms:260, play:"▶ 自動", pause:"❚❚ 暫停", onStart})
   */
  Lab.player = function (btn, opts) {
    var timer = null;
    var api = {
      playing: false,
      stop: function () {
        if (timer) { clearInterval(timer); timer = null; }
        api.playing = false; btn.textContent = opts.play;
      },
      start: function () {
        if (opts.onStart) opts.onStart();
        api.playing = true; btn.textContent = opts.pause;
        timer = setInterval(function () { if (opts.tick() === false) api.stop(); }, opts.ms || 260);
      }
    };
    btn.textContent = opts.play;
    btn.addEventListener("click", function () { if (api.playing) api.stop(); else api.start(); });
    return api;
  };

  /** 平方刻度滑桿：低段細、高段粗 */
  Lab.sqScale = function (max) {
    return {
      toN: function (v) { return Math.max(1, Math.round(1 + Math.pow(v / 100, 2) * (max - 1))); },
      fromN: function (n) { return Math.round(Math.sqrt((n - 1) / (max - 1)) * 100); }
    };
  };

  global.Lab = Lab;
})(window);
