#!/usr/bin/env python3
# Copyright (c) Meta Platforms, Inc. and affiliates.

import labgraph as lg
from typing import List, Tuple

Connection = List[str]

class DynamicGraph(lg.Graph):

    """
    DynamicGraph, allows you to construct a Graph object based on run-time parameters.
    `class ExampleGraph(DynamicGraph):`

    Use ExampleGraph.add_node() to register nodes.
    The `connections` parameter is expected to be a list with 4 strings:
    `[Node1Name, Node1TopicName, Node2Name, Node2TopicName]`

    Example:
        `ExampleGraph.add_node("TestNode2", TestNode2, ["TestNode2", "INPUT", "TestNode1", "OUTPUT", TestNode2Config(...)])`
    """

    _connections: List[Connection] = []
    _configs: dict = {}
    _cls: type = None

    @classmethod
    def add_node(cls, name: str, _type: type, connection: List[Connection] = None, config: lg.Config = None) -> None:
        setattr(cls, name, None)
        cls.__annotations__[name] = _type
        cls.__children_types__[name] = _type

        if connection:
            cls._connections.append(connection)
        
        if config:
            cls._configs[name] = config

    @classmethod
    def add_connection(cls, connection: List[Connection]) -> None:
        cls._connections.append(connection)

    def setup(self) -> None:
        for key in type(self)._configs:
            self.__getattribute__(key).configure(type(self)._configs[key])

    def connections(self) -> lg.Connections:
        cons = []
        for con_list in type(self)._connections:
            node1: lg.Node = self.__getattribute__(con_list[0])
            node2: lg.Node = self.__getattribute__(con_list[2])
            cons.append((node1.__getattribute__(con_list[1]), node2.__getattribute__(con_list[3])))
        return tuple(cons)
    
    def process_modules(self) -> Tuple[lg.Module, ...]:
        mods = ()
        for key in type(self).__children_types__:
            mods += (self.__getattribute__(key),)
        return mods

class DynamicGroup(lg.Group):

    """
    DynamicGroup, allows you to construct a Group object based on run-time parameters.
    `class ExampleGroup(DynamicGroup):`
    
    Use ExampleGroup.add_node() to register nodes.
    The `connections` parameter is expected to be a list with 4 strings:
    `[Node1Name, Node1TopicName, Node2Name, Node2TopicName]`

    Example:
        `DynamicGroup.add_node("TestNode2", TestNode2, ["TestNode2", "INPUT", "TestNode1", "OUTPUT", TestNode2Config(...)])`
    """

    _connections: List[Connection] = []
    _configs: dict = {}

    @classmethod
    def add_node(cls, name: str, _type: type, connection: List[Connection] = None, config: lg.Config = None) -> None:
        setattr(cls, name, None)
        cls.__annotations__[name] = _type
        cls.__children_types__[name] = _type

        if connection:
            cls._connections.append(connection)
        
        if config:
            cls._configs[name] = config

    @classmethod
    def add_connection(cls, connection: List[Connection]) -> None:
        cls._connections.append(connection)

    @classmethod
    def add_topic(cls, name: str, topic: lg.Topic) -> None:
        setattr(cls, name, topic)

    def setup(self) -> None:
        for key in type(self)._configs:
            self.__getattribute__(key).configure(type(self)._configs[key])

    def connections(self) -> lg.Connections:
        cons = []
        for con_list in type(self)._connections:
            node1: lg.Node = self.__getattribute__(con_list[0])
            node2: lg.Node = self.__getattribute__(con_list[2])
            cons.append((node1.__getattribute__(con_list[1]), node2.__getattribute__(con_list[3])))
        return tuple(cons)