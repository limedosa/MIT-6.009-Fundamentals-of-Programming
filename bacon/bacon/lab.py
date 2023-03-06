"""
6.1010 Spring '23 Lab 3: Bacon Number
"""

#!/usr/bin/env python3

import pickle

# NO ADDITIONAL IMPORTS ALLOWED!

# helper function for transform data
# def read_text_file(file_path):
#     with open(file_path, 'r') as f:
#         contents = f.read()
#     return contents


def transform_data_original(raw_data):
    #     # new_list = []
    #     # for name in raw_data:
    #     #     new_list.append(name)
    #     # return new_list
    with open(raw_data, "rb") as name:
        names = pickle.load(name)
    return names


# transform_test = transform_data("resources/large.pickle")
# print(transform_test)#this was for testing, and it worked!
# lol = [[key, value] for key, value in names.items()]
# print(lol)
# return names #og
#     file = read_text_file(raw_data)
#     for name in file:
#         filereturn = [int(weight) for weight in elf.split(",")] ###list comprehension
# transform_data("resources/large.pickle")


def transform_data(raw_data):
    """
     MUCH BETTER!!!!!!!!!!!!!!!
    Updated from the original usage of the transform_data;
    doesn't return a list anymore; returns sets!
    """
    acted_together = {}
    actors = {}

    [
        (
            acted_together.setdefault(a1, set()).add(a2),
            acted_together.setdefault(a2, set()).add(a1),
            actors.setdefault(movie, set()).update({a1, a2}),
        )
        for a1, a2, movie in raw_data
    ]

    return {"acted_with": acted_together, "movie_actors": actors}


def reversed_data(raw_data):
    """HELPER FUNCTION for original transform data : reversed raw data
    returns a list of reversed actor names, can be indexed into!"""
    # with open(raw_data, "rb") as name:
    #     names = pickle.load(name)
    data = transform_data(raw_data)  # uses other helper function!!!!!!
    # print(list)
    reversed_list = [(actor2, actor1, movie) for actor1, actor2, movie in data]
    return reversed_list


# print (this[12]) #this was for testing, and it worked!


def acted_together(transformed_data, actor_id_1, actor_id_2):
    """PASSED!!!!!!!!!!!!!
    Returns: True if actors were in same film, and False otherwise"""
    # data = transform_data(transformed_data)
    # # print(data)#used for debugging
    # # for film in range (len(data)):
    # #     # print(data[1])
    # #     if actor_id_1 in film and actor_id_2 in film:
    # #         return True
    # # return False
    # # as it may turn out, this works for data being input both ways
    # for film in data:
    #     if actor_id_1 in film and actor_id_2 in film:
    #         return True
    # return False
    for set in transformed_data:
        if actor_id_1 == actor_id_2:
            return True
        elif actor_id_2 in transformed_data["acted_with"][actor_id_1]:
            return True
        return False


def make_list_names():
    """HELPER FUNCTION
    Makes a list of all the author names with their corresponding ID"""
    file_input = "resources/names.pickle"
    with open(file_input, "rb") as name:
        names = pickle.load(name)
    # print(names)
    lol = [[key, value] for key, value in names.items()]
    return lol

    # print(len(lol)) #checks out!


names_list = [make_list_names()]
# print(names_list)
name_file = "my_file.txt"

with open(
    "names.txt", "w"
) as file:  # converted this into txt list so i could find the names
    file.write("\n".join([str(item) for item in names_list]))
# ['Anne Helm', 83390] and ['Beatrice Winde', 168638]

# # print(names_list)
# find_name = "Anne Helm"
# for name in names_list:
#     if name[0] == find_name:
#         print(name)


def find_actor(find_name, names):
    """HELPER FUNCT but doesnt work"""
    # names_list = [make_list_names()]
    # names = names_list
    for name in names:
        if name[0] == find_name:
            return name


find_name = "Lola Brooks"
found_actor = find_actor(find_name, names_list)
# print(found_actor)

# if found_actor:
#     print(found_actor)

################### 4) Acting Together DONE HERE:########################
# step 1: find their ID's from name
# print(names_list["Anne Helm"]) => did not work
# ['Anne Helm', 83390] and ['Beatrice Winde', 168638]
# ['Pierre Johnsson', 572601] and ['Evan Glenn', 1059003]
# STEP 2: FInd out if they acted together
# print(acted_together("resources/small.pickle", 83390, 168638))

# print(acted_together("resources/small.pickle", 572601, 1059003))


# TESTING acted_together
# thisact = acted_together("resources/small.pickle", 3472, 89040)
# print(thisact)

# database = transform_data(transformed_data)
# for actor_id_1 in database:
#         if actor_id_1  == actor_id_2:
#             return True
# return False
# # raise NotImplementedError("Implement me!")


#
with open("resources/tiny.pickle", "rb") as f:
    tiny = pickle.load(f)
tiny_list = tiny
# print(tiny_list)
with open("resources/large.pickle", "rb") as f:
    large = pickle.load(f)
large_list = large
# print(large_list)


def actors_with_bacon_number(transformed_data, n):
    """param: data and n(bacon number desired)
    Returns: a Python set containing the ID numbers of all the actors
    with that Bacon number.
    Note that we'll define the Bacon number to be the smallest
    number of films separating a given
    actor from Kevin Bacon, whose actor ID is 4724"""
    coactors = transformed_data["acted_with"]
    bacon_id = 4724
    actors_visited = {bacon_id: None}
    actors_at_level = {bacon_id}
    for i in range(n):
        actors_at_next_level = set()
        for actor_id in actors_at_level:
            for coactor_id in coactors[actor_id]:
                if coactor_id not in actors_visited:
                    actors_visited[coactor_id] = actor_id
                    actors_at_next_level.add(coactor_id)
        if not actors_at_next_level:
            return set()
        actors_at_level = actors_at_next_level
    return actors_at_level
    # data = transform_data(transformed_data)
    # bacon =  4724
    # actor_ids = set()
    # count = 1
    # for n in data:
    #     if n == bacon:
    #         count == 1
    #     else:
    #         count += 1
    # return count
    # TODO: parse `transformed_data` to get relevant
    # information about actors and movies
    # TODO: use BFS to calculate the Bacon number for each actor
    # TODO: filter the actors based on their Bacon number and
    # add their IDs to `actor_ids`


def bacon_path(transformed_data, actor_id):
    # raise NotImplementedError("Implement me!")
    path = actor_to_actor_path(transformed_data, 4724, actor_id)
    return path

def actor_to_actor_path(transformed_data, actor_id_1, actor_id_2):
    # raise NotImplementedError("Implement me!")
    def goal_test(person):
        return person == actor_id_2

    coactors = transformed_data["acted_with"]
    actors_i = {actor_id_1: None}
    pos = {actor_id_1}
    while pos:
        new_level = set()
        for actor in pos:
            for other in coactors[actor]:
                if other not in actors_i:
                    actors_i[other] = actor
                    new_level.add(other)
                    if goal_test(other):
                        new_list = []
                        while other is not None:
                            new_list.append(other)
                            other = actors_i[other]
                        return new_list[::-1]
        pos = new_level
    return None


def actor_path(transformed_data, actor_id_1, goal_test_function):
    # raise NotImplementedError("Implement me!")
    """finds path from one actor to other"""
    coactors = transformed_data["acted_with"]
    actors_i = {actor_id_1: None}
    pos = {actor_id_1}
    while pos:
        new_level = set()
        for actor in pos:
            for neighbor in coactors[actor]:
                if neighbor not in actors_i:
                    actors_i[neighbor] = actor
                    new_level.add(neighbor)
                    if goal_test_function(neighbor):
                        path = []
                        while neighbor is not None:
                            path.append(neighbor)
                            neighbor = actors_i[neighbor]
                        return path[::-1]
        pos = new_level
    return None



def actors_connecting_films(transformed_data, film1, film2):
    # raise NotImplementedError("Implement me!")
    actors = transformed_data["movie_actors"]
    try:
        paths = [
            actor_path(transformed_data, actor, lambda person: person in actors[film2])
            for actor in actors[film1]
        ]
        shortest_path = min(filter(None, paths), key=len)
        return shortest_path
    except ValueError:
        return None


# with open("resources/names.pickle", "rb") as name:
#     names = pickle.load(name)
# # print(names)
#     lol = [[key, value] for key, value in names.items()]
#     print(len(lol))


if __name__ == "__main__":
    with open("resources/large.pickle", "rb") as f:
        large_pickle = pickle.load(f)

    # print(large_pickle)
    # print(len(smalldb))

    # bacon/resources/small.pickle
    # additional code here will be run only when lab.py is invoked directly
    # (not when imported from test.py), so this is a good place to put code
    # used, for example, to generate the results for the online questions.


# with open("resources/names.pickle", "rb") as name:
#     names = pickle.load(name)
# # print(names)
#     lol = [[key, value] for key, value in names.items()]
#     print(len(lol))
# print(lol) #this works!!!!!!!!!!

# nameList = [(names)]
# print(nameList)
# my_dict = {'key1': 'value1', 'key2': 'value2', 'key3': 'value3'}
# nameDict = [names]
# nameDict = {}
# for i in names:

# print(nameDict)

# print(nameDict)
# key = "Zach Callison"
# my_value = names[key]

# print(my_value)

# valuec = '122547'
# keyc = None

# THIS WORKS TO RETURN KEY
# print(list(names.keys())[list(names.values()).index(122547)])

# for key, value in names.items():
#     if value == my_value:
#         keyc = key
#         break

# if keyc is not None:
#     print(f"The key associated with value '{valuec}' is '{keyc}'")
# else:
#     print(f"No key found for value '{valuec}'")
