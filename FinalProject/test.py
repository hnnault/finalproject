from ursina import *

app = Ursina()

e = Entity(model='cube', collider='box', position=Vec3(-8,0,0), scale=(5,1,1))
e.collider = BoxCollider(e, center=Vec3(0,0,0), size=Vec3(5,1,1))

q = Entity(model='cube', collider='box', scale=(2,1,1))
q.collider = BoxCollider(q, center=Vec3(0,0,0), size=Vec3(2,1,1))

def my_update():
    e.x += 1 * time.dt # dt is short for delta time, the duration since the last frame.
    q.x -= 1 * time.dt

    if e.intersects(e).hit:
        print("hit")

e.update = my_update

app.run()