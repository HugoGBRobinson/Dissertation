import pygame

import drone
import env
import groundstation
import lidar
import random


def main():
    """
    The main function sets up the
    :return:
    """
    count = 0
    environment = env.BuildEnvironment((600, 1200))
    environment.originalMap = environment.map.copy()
    environment.map.fill((0, 0, 0))
    environment.infomap = environment.map.copy()

    num_of_drones = 5

    ground_station = groundstation.GroundStation(environment, num_of_drones)

    drones = []
    drone_deflects_clockwise = True
    for i in range(num_of_drones):
        drones.append(
            drone.Drone(i, (100, 100), lidar.Sensor(200, pygame.surfarray.array2d(environment.originalMap)),
                        environment.drones, ground_station, environment,
                        drone_deflects_clockwise))  # environemnt added for testing
        if drone_deflects_clockwise == True:
            drone_deflects_clockwise = False
        else:
            drone_deflects_clockwise = True

    running = True

    environment.set_drones_in_env(drones)
    ground_station.mixed_exploration(drones=drones)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        for i in range(len(drones)):
            drones[i].sense_environment()
            ground_station.check_for_drones()
            environment.map.blit(environment.infomap, (0, 0))
            pygame.display.update()

        if count % 100 == 0:
            percentage = pecentage_map_explored(environment.originalMap, environment.infomap)
            print(percentage)
            if percentage > 85:
                print("-----------------------------------------------------------------------------------------------")
                print("The " + str(num_of_drones) + " drone(s) explored 85% of the environment in " + str(count)
                      + " iterations")
                print("-----------------------------------------------------------------------------------------------")
                break
        if count == 10000:
            percentage = pecentage_map_explored(environment.originalMap, environment.infomap)
            print("-----------------------------------------------------------------------------------------------")
            print("The " + str(num_of_drones) + " drone(s) explored + " + str(
                int(percentage)) + "% of the environment in " + str(count)
                  + " iterations")
            print("-----------------------------------------------------------------------------------------------")

        # remove_drone(drones)
        print(count)
        count += 1


def pecentage_map_explored(whole_map, current_map):
    whole_map = pygame.surfarray.pixels2d(whole_map)
    # 16711680
    whole_map_count = list(whole_map.flatten()).count(0)
    current_map = pygame.surfarray.pixels2d(current_map)
    current_map = list(current_map.flatten())
    current_map_count = len([colour for colour in current_map if colour == 16711680])
    return ((current_map_count / whole_map_count) * 100)


def run_drones(drone):
    drone.sense_environment()


def remove_drone(drones):
    num = random.randint(0, 100000)
    if num == 1:
        drones.remove(random.randint(0, len(drones)))


if __name__ == '__main__':
    main()
