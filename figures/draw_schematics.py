"""Vector drawing primitives; copied into each independent project generator."""
import argparse
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon, Circle, FancyArrowPatch

plt.rcParams.update({'font.family':'STIXGeneral', 'mathtext.fontset':'stix',
                     'font.size':9, 'pdf.fonttype':42, 'ps.fonttype':42,
                     'text.usetex':False, 'axes.unicode_minus':False})
CM = 1 / 2.54

class Drawing:
    def __init__(self, bounds):
        x0,y0,x1,y1 = bounds
        self.fig = plt.figure(figsize=((x1-x0)*CM,(y1-y0)*CM))
        self.ax = self.fig.add_axes([0,0,1,1], xlim=(x0,x1), ylim=(y0,y1))
        self.ax.set_aspect('equal'); self.ax.axis('off')
        self.nodes = {}
        self.labels = []

    def text(self,x,y,label,size=9,ha='center',va='center'):
        artist=self.ax.text(x,y,label,fontsize=size,ha=ha,va=va,
                            linespacing=1.15,clip_on=False,zorder=4)
        self.labels.append([artist,None])
        return artist

    def box(self,name,x,y,w,h,label,dashed=False,shape='rect',size=9):
        style = {'edgecolor':'black','facecolor':'white','linewidth':.55,
                 'linestyle':(0,(4,3)) if dashed else 'solid', 'zorder':2}
        if shape == 'diamond':
            obj = Polygon([(x-w/2,y),(x,y+h/2),(x+w/2,y),(x,y-h/2)],**style)
        elif shape == 'circle': obj = Circle((x,y),w/2,**style)
        else: obj = Rectangle((x-w/2,y-h/2),w,h,**style)
        self.ax.add_patch(obj); self.text(x,y,label,size)
        self.labels[-1][1]=(x-w/2,y-h/2,x+w/2,y+h/2)
        self.nodes[name] = (x,y,w,h,shape)

    def point(self,name,side):
        x,y,w,h,_ = self.nodes[name]
        return {'n':(x,y+h/2),'s':(x,y-h/2),'e':(x+w/2,y),
                'w':(x-w/2,y),'nw':(x-w/2,y+h/2),
                'ne':(x+w/2,y+h/2),'c':(x,y)}[side]

    def line(self,points,dashed=False):
        xs,ys=zip(*points)
        self.ax.plot(xs,ys,color='black',linewidth=.55,
                     linestyle=(0,(4,3)) if dashed else 'solid',zorder=1)

    def arrow(self,p,q,dashed=False,via=()):
        points=[p,*via,q]
        if via:self.line(points[:-1],dashed)
        self.ax.add_patch(FancyArrowPatch(points[-2],points[-1],
                         arrowstyle='-|>',mutation_scale=7.5,linewidth=.55,
                         color='black',shrinkA=0,shrinkB=0,
                         linestyle=(0,(4,3)) if dashed else 'solid',zorder=1))

    def edge(self,a,b,sa='s',sb='n',**kwargs):
        self.arrow(self.point(a,sa),self.point(b,sb),**kwargs)

    def frame(self,x,y,w,h):
        self.ax.add_patch(Rectangle((x,y),w,h,fill=False,edgecolor='black',
                                   linewidth=.55,linestyle=(0,(4,3)),zorder=0))

    def save(self,out,name):
        # Fixed physical canvas: do not enlarge or rasterize the scientific figure.
        self.fig.canvas.draw()
        renderer=self.fig.canvas.get_renderer()
        x0,x1=self.ax.get_xlim();y0,y1=self.ax.get_ylim()
        for artist,node in self.labels:
            b=artist.get_window_extent(renderer).transformed(self.ax.transData.inverted())
            if b.x0<x0-.02 or b.x1>x1+.02 or b.y0<y0-.02 or b.y1>y1+.02:
                raise ValueError(name+': clipped label '+repr(artist.get_text()))
            if node and (b.x0<node[0]-.02 or b.x1>node[2]+.02 or b.y0<node[1]-.02 or b.y1>node[3]+.02):
                raise ValueError(name+': label exceeds node '+repr(artist.get_text()))
        self.fig.savefig(out/(name+'.pdf'),format='pdf',
                         metadata={'Creator':'Python Matplotlib','Producer':None,
                                   'CreationDate':None,'ModDate':None})
        plt.close(self.fig)


def model(out):
    d=Drawing((-.2,-.2,8.3,5.0))
    for name,x,y,w,h,label in [
        ('pred',1,4,1.8,.8,'prediction\n'+r'$\hat\theta$'),
        ('cache',3.7,4,2.1,.8,'execute prefix\ncache $c$'),
        ('reveal',6.6,4,1.8,.8,'reveal\n'+r'$\theta$'),
        ('old',1,1.8,1.8,.8,'private\ncached slots'),
        ('repair',3.7,1.8,2.1,.8,'choose $R$\none repair pass'),
        ('suffix',6.6,1.8,2.5,.8,'fresh suffix\natomic observe'),
        ('mix',6.6,.35,2.5,.55,r'$\mathrm{Mix}(\theta,R)$')]:
        d.box(name,x,y,w,h,label,size=8)
    d.edge('pred','cache','e','w');d.edge('cache','reveal','e','w')
    d.text(5.2,4.6,'barrier',8)
    d.edge('reveal','repair','s','n',via=((6.6,2.8),(3.7,2.8)))
    d.edge('old','repair','e','w');d.edge('repair','suffix','e','w');d.edge('suffix','mix')
    d.save(out,'model-overview')


def cancellation(out):
    d=Drawing((0,-.65,8.6,3.1));d.text(4.3,2.6,r'$d:0\to1$',8.5)
    for name,x,label in [('s1',1.5,r'$s_1=d$'+'\n'+r'$0\to1$'),('s2',4.3,r'$s_2=d\oplus d$'+'\n'+r'$0\to0$'),('sp',7.1,r'$s_p=d\oplus d$'+'\n'+r'$0\to0$')]:
        d.box(name,x,.9,2.3,1.0,label,size=8)
        d.arrow((4.3,2.35),d.point(name,'n'))
    d.frame(.15,.2,8.3,1.4)
    d.text(4.3,-.25,r'Declared descendants $D=\{s_1,\ldots,s_p\}$',8)
    d.save(out,'invalidation-cancellation')


def gap(out):
    d=Drawing((-2.6,-5,6.2,.7));d.text(2.4,.35,'$d$',8.5)
    for i,x in enumerate((0,2.4,4.8),1):
        s,a='s'+str(i),'a'+str(i)
        d.box(s,x,-1,1.2,.55,'$s_'+str(i)+'$',size=8)
        d.arrow((2.4,.12),d.point(s,'n'))
        d.box(a,x,-2.2,.45,.45,r'$\wedge$',shape='circle',size=8)
        d.edge(s,a);d.text(x-.9,-2.2,'$u_'+str(i)+'$',8)
        d.arrow((x-.65,-2.2),d.point(a,'w'))
    d.frame(-.75,-1.45,6.3,.9);d.text(-1.5,-1,'cached\nCOPY slots',8)
    d.box('o12',1.2,-3.05,.45,.45,r'$\vee$',shape='circle',size=8)
    d.box('o',2.4,-3.8,.45,.45,r'$\vee$',shape='circle',size=8)
    d.edge('a1','o12');d.edge('a2','o12');d.edge('o12','o');d.edge('a3','o')
    d.frame(-1.25,-4.15,6.8,2.45);d.text(5.5,-4.4,'fresh suffix',8,ha='right')
    d.text(2.4,-4.7,'$y$',8);d.arrow(d.point('o','s'),(2.4,-4.52))
    d.save(out,'gap-star')


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,default=Path(__file__).resolve().parent)
    a=parser.parse_args();a.output.mkdir(parents=True,exist_ok=True)
    model(a.output);cancellation(a.output);gap(a.output)


