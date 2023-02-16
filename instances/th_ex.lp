assumption(a).
assumption(b).
assumption(c).
assumption(d).

assumption(e).
assumption(f).
assumption(g).
assumption(i).
assumption(h).

contrary(c,xc).
contrary(b,xb).
contrary(d,xd).
contrary(e,xe).
contrary(f,xf).
contrary(g,xg).
contrary(i,xi).
contrary(h,xh).
contrary(a,xa).

%p:-a,b,q.
head(p1,p).
body(p1,a).
body(p1,b).
body(p1,q).

%q:-xe,r.
head(q1,q).
body(q1,xe).
body(q1,r).

%q:-i.
head(q2,q).
body(q2,i).

%r:-c.
head(r1,r).
body(r1,c).

%r:-d.
head(r2,r).
body(r2,d).

%xe:-c.
head(xe1,xe).
body(xe1,c).

%xf:-xe.
head(xf1,xf).
body(xf1,xe).

%xi:-g.
head(xi1,xi).
body(xi1,g).

%xa:-e,v.
head(xa1,xa).
body(xa1,e).
body(xa1,v).

%xa:-z.
head(xa2,xa).
body(xa2,z).

%v:-h.
head(v1,v).
body(v1,h).

%v:-i.
head(v2,v).
body(v2,i).

%z:-f.
head(z1,z).
body(z1,f).

