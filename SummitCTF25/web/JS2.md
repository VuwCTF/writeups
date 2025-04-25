This challenge takes on a completely new and innovative approach 🫨 . Yes that is sarcasm.

You check the javascript and run it through a deobfuscator to find the flag.

Attatched is the obfuscated code.

And here is the deobfuscated code:
```js
var e = function () {
  var W = true;
  return function (J, v) {
    var g = W ? function () {
      if (v) {
        var l = v.apply(J, arguments);
        v = null;
        return l;
      }
    } : function () {};
    W = false;
    return g;
  };
}();
var O = e(this, function () {
  var W = function () {
    var x;
    try {
      x = Function("return (function() {}.constructor(\"return this\")( ));")();
    } catch (q) {
      x = window;
    }
    return x;
  };
  var J = W();
  var v = J.console = J.console || {};
  var g = ["log", "warn", "info", "error", "exception", "table", "trace"];
  for (var F = 0; F < g.length; F++) {
    var i = e.constructor.prototype.bind(e);
    var E = g[F];
    var z = v[E] || i;
    i.__proto__ = e.bind(e);
    i.toString = z.toString.bind(z);
    v[E] = i;
  }
});
O();
window.checkPassword = function () {
  var W = document.getElementById("password").value;
  if (W === "SummitCTF{Y0u_Found_Th3_P4ssw0rd_348}") {
    alert("Correct password!");
  } else {
    alert("Wrong password. Please try again.");
  }
};```

Oh hey, there's the flag, what a surprise! SummitCTF{Y0u_Found_Th3_P4ssw0rd_348}
