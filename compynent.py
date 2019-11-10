"""
A library to implement entity-component-system for python.
"""

import warnings


class EntityManager(object):
    """
    Manages creating entities, assigning components
    to them, accessing the components and adding systems.

    An instance of this class will generally be the
    main point of interaction with this library.
    """
    
    #Record the number of entities created for their unique integer ids
    number = 0

    def __init__(self):
        #Entities are id:list of components
        self.entities = {}
        #Systems are object:order
        self.systems = {}

    def create_entity(self, *initial_components):
        """
        Return an integer which is a unique identifier for an
        entity.

        As optional parameters, an arbitrary number of
        components can be passed to create an entity with those
        components initially.
        """
        EntityManager.number += 1
        unique_id = EntityManager.number
        self.entities[unique_id] = []
        for component in initial_components:
            self.entities[unique_id].append(component)
        return unique_id

    def delete_entity(self, entity):
        """Remove the entity referred to by an integer."""
        del self.entities[entity]

    def get_entities(self):
        """Return a list of the identifiers for all entities."""
        return list(self.entities)

    def add_component(self, entity, component):
        """Add a component to an entity"""
        self.entities[entity].append(component)

    def get_component(self, entity, component_type):
        """Return the component of the type component_type on
        entity. If it does not exist, None is returned."""
        for component in self.entities[entity]:
            if type(component) == component_type:
                return component
        return None

    def remove_component(self, entity, component_type):
        """Remove a component from an entity."""
        for component in self.entities[entity]:
            if type(component) == component_type:
                try:
                    component.cleanup()
                except AttributeError:
                    #Not all components need/have a cleanup method
                    pass
                self.entities[entity].remove(component)
                return

    def has_component(self, entity, *component_types):
        """
        Return a bool indicating if the passed entity contains
        all of the passed components.
        """
        types_present = []
        append = list.append
        for component in self.entities[entity]:
            append(types_present, type(component))
        for required_type in component_types:
            if required_type not in types_present:
                return False
        return True

    def clear_entity(self, entity):
        """Remove all components from an entity."""
        self.entities[entity] = []

    def add_system(self, system, order=5):
        """Create a system from a system object (an object with
        an update() method). The order parameter controls the
        order in which the systems are called, with lower numbers
        being run first.

        All systems are called when do_frame is called on EntityManager."""
        assert hasattr(system, "update"), "Systems must have an update() method"
        assert type(order) == int, "Order must be an integer"
        self.systems[system] = order

    def do_frame(self, *data):
        """Call update for all systems, optionally passing data to them."""
        for system in sorted(self.systems, key=self.systems.get):
            system.update()

    def get_entities_with_component(self, *component_types):
        """Return a list of all entities that contain a given component."""
        #Access the methods outside the loop for performance reasons
        has_component = self.has_component
        append = list.append
        results = []
        for entity in self.entities:
            if has_component(entity, *component_types):
                append(results, entity)
        return results
       