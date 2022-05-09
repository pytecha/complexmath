from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from sympy import *

# Create your views here.

(x, y, z), i, e = symbols("x y z", real=True), I, E
locals = {"pi":pi,"e":e,"i":i,"x":x,"y":y,"z":z}

def symcalc(request):
    return render(request, "symcapp/symcalc.html")

def math(request):
    ctype = request.POST["ctype"]
    f = sympify(request.POST["f"], locals=locals)
    a = Symbol(request.POST["a"], real=True)
    
    info = [["#sol1","Answer:"], ["#sol2","Real Part:"], ["#sol3","Img Part:"]]
    if ctype == "diff":
        _f = simplify(diff(f, a))
        result = [[j, latex(_i)] for _i, j in zip([_f,re(_f), im(_f)], info)]
    elif ctype == "limit":
        c = sympify(request.POST["c"], locals=locals)
        _f = simplify(limit(f,a,c))
        result = [[j,latex(_i)] for _i, j in zip([_f,re(_f), im(_f)], info)]
    elif ctype == "pdiff":
         _re, _im = re(f), im(f)
         _rex, _rey = diff(_re, x), diff(_re, y)
         _imx, _imy = diff(_im, x), diff(_im, y)
         isanalitic = simplify(_rex-_imy) == 0 and simplify(_rey+_imx) == 0
         info = [["#sol1","Real Part:"], ["#sol2","Img Part:"], ["#sol3",r"\frac{\partial u}{\partial x}:"], ["#sol4",r"\frac{\partial u}{\partial y}:"], ["#sol5",r"\frac{\partial v}{\partial x}:"], ["#sol6",r"\frac{\partial v}{\partial y}:"]]
         result = [[j,latex(simplify(_i))] for _i, j in zip([_re, _im, _rex, _rey, _imx, _imy], info)]+[[["#sol7", "Is Analytic:"], latex(isanalitic)]]
    
    return JsonResponse({"result": result})