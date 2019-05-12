<h1 style="color:#3423ff; font-family:cursive">
    ComPyNent
</h1>

Entity-Component-System (ECS) framework for Python 3+. It aims to be flexible, performant and easy to use and learn, with a specific
emphasis on game development. There is currently an exmaple of how to integrate it with the [Panda3D](https://panda3d.org) game engine, although it can also be used in conjunction with other frameworks such as [Pygame](https://pygame.org) or [Pyglet](https://bitbucket.org/pyglet/pyglet/wiki/Home).

## How to use
This is a one-file library: just add `compynent.py` to your project, and import it with `import compynent`.

## Overview
For an explanation of how ECS works and what the motivation for it is, read [this article](https://www.gamedev.net/articles/programming/general-and-gameplay-programming/understanding-component-entity-systems-r3013/).
The implementation in ComPyNent uses the approach by which entities are simply integers that refer to a list of the components
attached to them.

The main class is the EntityManager class. Normally, you only need to instantiate it once.

- To create an __entity__, use the `create_entity` method of EntityManager. It optionally accepts inital components as parameters
- __Components__ are simply objects with data as its members
- A __system__ can be a function or method that is added via the `add_system` method of EntityManager, and it is called each time that the `do_frame` method of that instance of EntityManager is called

Example:
```python
import pycomponent

ecs = pycomponent.EntityManager()

class MessageComponent:
    def __init__(self, message):
        self.message = message

entity = ecs.create_entity()
component = MessageComponent()
ecs.add_component(entity, component)

def message_system():
    for entity in ecs.get_entities():
        if entity.has_component(MessageComponent):
            print(ecs.get_component(entity, MessageComponent)
            
ecs.add_system(message_system)

while True:
    ecs.do_frame()
```

## Contributing
See [CONTRIBUTING.md](https://github.com/typewriter1/ComPyNent/blob/master/CONTRIBUTING.md).

# License
[The Unlicense](https://unlicense.org/)
