import subprocess, itertools, re, math
# bridged-pot EQ: inverting unity stage, each band pot from VIN to VOUT, wiper -> band network -> -in
def net(h,m,l, P):
    # h,m,l: wiper position 0 (=VIN end, boost) .. 1 (=VOUT end, cut)
    def pot(name,a,b,w,x,R=10e3):
        x=min(max(x,1e-4),1-1e-4)
        return f"R{name}a {a} {w} {R*x}\nR{name}b {w} {b} {R*(1-x)}\n"
    s=f"""* eq
Vin vin 0 AC 1
Rin vin n {P['Rin']}
Rf out n {P['Rf']}
E1 out 0 0 n 1e6
"""
    s+=pot('h','vin','out','wh',h)+f"Rh1 wh xh {P['Rh']}\nCh xh n {P['Ch']}\n"
    s+=pot('l','vin','out','wl',l)+f"Rl1 wl xl {P['Rl1']}\nCl xl 0 {P['Cl']}\nRl2 xl n {P['Rl2']}\n"
    s+=pot('m','vin','out','wm',m)+f"Rm1 wm xm {P['Rm1']}\nCm2 xm 0 {P['Cm2']}\nCm1 xm ym {P['Cm1']}\nRm2 ym n {P['Rm2']}\n"
    s+=".ac dec 20 20 20k\n.control\nrun\nprint vdb(out)\n.endc\n.end\n"
    return s
def run(h,m,l,P):
    open('e.cir','w').write(net(h,m,l,P))
    o=subprocess.run(['ngspice','-b','e.cir'],capture_output=True,text=True).stdout
    d={}
    for line in o.splitlines():
        p=line.split()
        if len(p)==3 and p[0].isdigit():
            d[float(p[1])]=float(p[2])
    return d
def at(d,f): 
    k=min(d,key=lambda x:abs(math.log(x/f))); return d[k]
P=dict(Rin=10e3,Rf=10e3,Rh=2.2e3,Ch=10e-9,Rl1=1.5e3,Cl=1e-6,Rl2=1.5e3,Rm1=1.5e3,Cm2=22e-9,Cm1=47e-9,Rm2=1.5e3)
import sys
if __name__=="__main__":
 for name,(h,m,l) in {'flat':(.5,.5,.5),'hi+':(0,.5,.5),'hi-':(1,.5,.5),'mid+':(.5,0,.5),'mid-':(.5,1,.5),'lo+':(.5,.5,0),'lo-':(.5,.5,1),'all+':(0,0,0)}.items():
    d=run(h,m,l,P)
    print(f"{name:5}", '  '.join(f"{f}:{at(d,f):+6.1f}" for f in (50,100,300,1000,2500,5000,10000,15000)))
