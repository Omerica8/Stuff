import subprocess, math, itertools
def run(x,P,gyr=False):
    x=min(max(x,1e-4),1-1e-4)
    s=f"""* mid cell
Vin vin 0 AC 1
R1a vin p {P['R1']}
R1b out n {P['R1']}
E1 out 0 p n 1e6
Rpa p w {10e3*x}
Rpb w n {10e3*(1-x)}
Rq w a {P['Rq']}
Cs a b {P['C']}
"""
    if gyr:
        # gyrator: L = Rs*Rg*Cg, series loss Rs
        s+=f"Cg b g {P['Cg']}\nRg g 0 {P['Rg']}\nE2 o2 0 g 0 1\nRs o2 b {P['Rs']}\n"
    else:
        s+=f"L1 b 0 {P['L']}\n"
    s+=".ac dec 40 20 20k\n.control\nrun\nprint vdb(out)\n.endc\n.end\n"
    open('m.cir','w').write(s)
    o=subprocess.run(['ngspice','-b','m.cir'],capture_output=True,text=True).stdout
    d={}
    for line in o.splitlines():
        p=line.split()
        if len(p)==3 and p[0].isdigit(): d[float(p[1])]=float(p[2])
    return d
def at(d,f): return d[min(d,key=lambda k:abs(math.log(k/f)))]
def bw(d):
    pk=max(d,key=lambda k:abs(d[k])); g=d[pk]; half=g/2
    fs=[f for f in d if abs(d[f])>=abs(half)]
    return pk,g,min(fs),max(fs)
if __name__=="__main__":
    f0=2500
    for R1,Rq,C in itertools.product([1e3,2.2e3,3.3e3],[100,220,470],[22e-9,47e-9]):
        L=1/((2*math.pi*f0)**2*C)
        P=dict(R1=R1,Rq=Rq,C=C,L=L)
        d=run(0,P); pk,g,lo,hi=bw(d)
        print(R1,Rq,C,f"L={L*1e3:.0f}mH",'end0',round(pk),round(g,1),'halfgain band',round(lo),round(hi),'end1',round(at(run(1,P),f0),1),'ctr',round(at(run(.5,P),f0),1))
