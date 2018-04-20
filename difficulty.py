

class Settings:
    """ Holds the game setting parameters for the game. Specialy, those related to difficulty

    Attributes:
        group_pipe_separation : More distance between pipes is easier to play,
                                giving more time to react to changing gap locations. Make sure that the
                                distance is such that the pipe is generated at a distance (i.e, outside the
                                screen width) that is safe for the player (bird) to react to.

        pipe_gap        : The distance between the upper pipe and the lower pipe.
                          Narrower gaps are more difficult as the bird has less room to
                          maneuver, requiring better motor skills.

        pipe_width      : Wider pipes increase difficulty as the bird spends more time in the narrow pipe gap.

        pipe_gap_loc_range : The pipe gap locations are uniformly randomly distributed in a range somewhere
                             between the ceiling and the floor. Larger ranges are harder because there is
                             more distance to travel between a high gap and a low gap.

        gravity           : Acceleration of the bird in the y direction, subtracted from the bird's y velocity
                              each frame. Higher gravity causes the bird to drop faster, lowering the margin of
                              error.

        jump_vel           : When the bird flaps, its vertical velocity is set to jump_vel, making it jump upward.
                              Higher velocity makes higher jumps.

        bird_vel           : Speed at which the bird travels to the right (alternately, the speed at which pipes
                                travel to the left).

        world_width        : Screen width. In Flappy Bird, this is defined by the display resolution.

        world_height       : Distance between ceiling and floor. In Flappy Bird, this is defined by the
                              display resolution.

        bird_width         : width of the bird's hit box. The wider and taller the bird, the harder it
                            will be to jump through gaps.

        bird_height        : height of the bird's hit box. The wider and taller the bird, the harder it
                            will be to jump through gaps.
        """
    def __init__(self, group_pipe_separation=0.5, pipe_width=0, pipe_gap_loc_range=0, gravity=1.1, jump_vel=6,
                 bird_vel=4.0, bird_width=0, bird_height=0, pipe_gap=150, world_height=512, world_width=288):
        self.group_pipe_separation = group_pipe_separation      # OK
        self.pipe_gap = pipe_gap                                # OK
        self.pipe_width = pipe_width
        self.pipe_gap_loc_range = pipe_gap_loc_range
        self.gravity = gravity                                  # OK
        self.jump_vel = jump_vel                                # OK
        self.bird_vel = bird_vel                                # OK
        self.world_width = world_width                          # OK
        self.world_height = world_height                        # OK
        self.bird_width = bird_width
        self.bird_height = bird_height


DIFFICULTY = Settings(group_pipe_separation=150, jump_vel=7)