import compynent

from panda3d import core
from direct.showbase.ShowBase import ShowBase

class ModelComponent:
    def __init__(self, path, parent):
        self.model = loader.load_model(path)
        self.model.reparent_to(parent)
          
class PosComponent:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z
        
class PosSystem:
    def __init__(self, ecs):
        self.ecs = ecs
        
    def update(self):
        for entity in self.ecs.get_entities_with_component(ModelComponent, PosComponent):
            model = self.ecs.get_component(entity, ModelComponent)
            pos = self.ecs.get_component(entity, PosComponent)
            model.model.set_pos(pos.x, pos.y, pos.z)

class Demo(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        
        self.ecs = ecs = compynent.EntityManager()
        self.player = self.ecs.create_entity()
        self.ecs.add_component(self.player, ModelComponent("models/box.egg", self.render))
        self.ecs.add_component(self.player, PosComponent(x = 0, y = 0, z = 5))

        ecs.add_system(PosSystem(self.ecs))
        self.task_mgr.add(self.frame_update_task, "Do ECS Frame")
                   
    def frame_update_task(self, task):
        self.ecs.do_frame()
        return task.cont

demo = Demo()
demo.run()