#!/usr/bin/python
# -*- coding: utf-8 -*-


from __future__ import print_function
from modules.timers import named_sub_timers




def get_step(t):

  def step(dl):

    dl.structure()
    t.t('str')
    dl.cand_spawn(ratio=0.05)
    t.t('spw')

    dl.forces()
    t.t('frc')

    return True

  return step

def get_wrap(dl, colors, t):

  from numpy import pi
  from fn import Fn
  twopi = pi*2

  xy = dl.xy
  cand_count = dl.cand_count

  fn = Fn(prefix='./res/', postfix='.png')

  step = get_step(t)

  def wrap(render):

    res = step(dl)

    if dl.itt % 10 != 0:
      return res

    print('itt', dl.itt, 'num', dl.num)
    t.p()
    num = dl.num
    render.set_line_width(dl.one)
    arc = render.ctx.arc
    fill = render.ctx.fill

    render.clear_canvas()

    cand_flag = cand_count[:num,0] < dl.cand_count_limit

    render.ctx.set_source_rgba(*colors['light'])
    for i in xrange(num):


      if cand_flag[i]:
        render.ctx.set_source_rgba(*colors['cyan'])
      else:
        render.ctx.set_source_rgba(*colors['light'])
      arc(xy[i,0], xy[i,1], dl.one*2, 0, twopi)
      fill()


    render.write_to_png(fn.name())

    return res

  return wrap



def main():

  from numpy import array
  from modules.differentialLattice import DifferentialLattice
  from render.render import Animate

  colors = {
    'back': [1,1,1,1],
    'front': [0,0,0,0.7],
    'cyan': [0,0.6,0.6,0.6],
    'light': [0,0,0,0.6],
  }

  size = 500
  one = 1.0/size

  # stp = 5e-6
  stp = 1e-4
  spring_stp = 1.0
  reject_stp = 1.0
  attract_stp = reject_stp

  max_capacity = 6

  cand_count_limit = 5

  node_rad = 3.0*one
  disconnect_rad = 2.0*node_rad
  inner_influence_rad = 2.0*node_rad
  outer_influence_rad = 8.0*node_rad

  t = named_sub_timers('dl')



  DL = DifferentialLattice(
    size,
    stp,
    spring_stp,
    reject_stp,
    attract_stp,
    max_capacity,
    cand_count_limit,
    node_rad,
    disconnect_rad,
    inner_influence_rad,
    outer_influence_rad
  )

  DL.spawn(100, xy=array([[0.5,0.5]]),dst=node_rad*0.8, rad=0.1)

  render = Animate(size, colors['back'], colors['front'], get_wrap(DL, colors, t))
  render.start()


if __name__ == '__main__':

  main()

