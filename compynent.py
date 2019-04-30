"""
A library to implement entity-component-system for python.
"""

import warnings


class EntityManager(object):
    """
    Manages creating entities, assigning components
    to them and accessing the components.

    An instance of this class will generally be the
    main point of interaction with this library.
    """

    number = 0

    def __init__(self):
        self.entities = {}
        self.systems = []

    def create_entity(self, *initial_components):
        """
        Returns a integer which is a unique identifier to an
        entity.

        An optional list of components can be passed to create
        an entity with those components.
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
        entity entity. If it does not exist, None is returned."""
        for component in self.entities[entity]:
            if type(component) == component_type:
                return component

    def remove_component(self, entity, component_type):
        """Remove a component from an entity."""
        for component in self.entities[entity]:
            if type(component) == component_type:
                self.entities[entity].remove(component)
                return

    def has_component(self, entity, *component_types):
        """
        Return a bool indicating if the passed entity contains
        a every one of the passed components.
        """
        types_present = []
        for component in self.entities[entity]:
            types_present.append(type(component))
        for required_type in component_types:
            if required_type not in types_present:
                return False
        return True

    def clear_entity(self, entity):
        """Removes all components from an entity."""
        self.entities[entity] = []

    def add_system(self, function):
        """Creates a system from a function.

        All systems are called once per frame."""
        self.systems.append(function)

    def do_frame(self, *data):
        """Calls all systems, optionally passing data to them."""
        for function in self.systems:
            function(*data)

    def get_entities_with_component(self, *component_types):
        """Returns a list of all entities that contain a given component."""
        #Access the methods outside the loop for performance reasons
        has_component = self.has_component
        append = list.append
        results = []
        for entity in self.entities:
            if has_component(entity, *component_types):
                append(results, entity)
        return results
