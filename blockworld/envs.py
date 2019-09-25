from dm_control import suite
import numpy as np


class RefTwoBlocksEnv:

    def __init__(self, env_name='blocks', task='stack_2', render_kwargs=dict(width=64, height=64, camera_id=0)):

        self.dm_env = suite.load(env_name, task)
        self.physics = self.dm_env.physics
        self.model = self.physics.named.model
        self.data = self.physics.named.data
        self.box_size = self.model.geom_size['box0', 0]
        self.render_kwargs = render_kwargs
        self.red = np.array([246., 91., 75.])/255.
        self.green = np.array([93., 205., 189.])/255.

    def set_block_pos(self, box0=[None, None, None], box1=[None, None, None]):

        xyz0 = [self.data.qpos["box0_x"].copy(),
                self.data.qpos["box0_y"].copy(),
                self.data.qpos["box0_z"].copy()]

        xyz1 = [self.data.qpos["box1_x"].copy(),
                self.data.qpos["box1_y"].copy(),
                self.data.qpos["box1_z"].copy()]

        with self.physics.reset_context():
            self.data.qpos["box0_x"] = xyz0[0] if box0[0] is None else box0[0]
            self.data.qpos["box0_y"] = 0.001 if box0[1] is None else box0[1]
            self.data.qpos["box0_z"] = xyz0[2] if box0[2] is None else box0[2]
            self.data.qpos["box1_x"] = xyz1[0] if box1[0] is None else box1[0]
            self.data.qpos["box1_y"] = 0.001 if box1[1] is None else box1[1]
            self.data.qpos["box1_z"] = xyz1[2] if box1[2] is None else box1[2]

    def render(self, **render_kwargs):
        kwargs = render_kwargs if render_kwargs else self.render_kwargs
        return self.dm_env.physics.render(**kwargs)

    def reset(self):
        ts = self.dm_env.reset()
        change_object_color(self, "self", self.red)
        change_object_color(self, "target", self.green)

    def step(self, a):
        return self.dm_env.step(a)


def change_object_color(env, obj, color):
    _MATERIALS = [obj]

    env.model.mat_rgba[_MATERIALS] = list(
        color)+[1.0]
