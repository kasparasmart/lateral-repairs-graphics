"""Lateral Repairs promo video — built and rendered headless with bpy (Blender 5.0).

Storyboard (24 fps, frames 1-200, ~8.3 s + freeze-frame hold added in ffmpeg):
  f1-115   CCTV-style camera travels through a pipe while a glowing applicator
           ring ahead of it lays a fresh resin liner on the pipe wall.
  f115-150 Camera flies out of the pipe mouth and arcs around to face it.
  f138-172 The Lateral Repairs logo launches out of the pipe, spins and settles
           centered in frame.
  f172-200 "MANUFACTURING PERFECTION" fades in at the bottom; the shot becomes
           a still picture (held as a freeze frame in the final video).

Usage:
  python3 promo_video.py                      # build scene, save .blend
  python3 promo_video.py --frame N            # build + render single frame N
  python3 promo_video.py --render START END   # build + render frame range
"""

import math
import sys

import bpy
from mathutils import Matrix, Vector

FPS = 24
FRAME_START = 1
FRAME_END = 200

PIPE_RADIUS = 1.0
PIPE_Z0 = -40.0   # closed/dark end
PIPE_Z1 = 0.6     # mouth (protrudes through the wall at z=0)

NAVY = (0.012, 0.075, 0.28, 1.0)
AMBER = (0.95, 0.45, 0.06, 1.0)
RESIN = (0.28, 0.16, 0.05, 1.0)

OUT_FRAMES = "/tmp/frames"


# ---------------------------------------------------------------- helpers
def ease_io(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3.0 - 2.0 * t)


def ease_out_back(t, s=1.35):
    t = max(0.0, min(1.0, t)) - 1.0
    return 1.0 + (s + 1.0) * t ** 3 + s * t * t


def lerp(a, b, t):
    return a + (b - a) * t


def clamp(v, lo, hi):
    return max(lo, min(hi, v))


def smooth_shade(obj):
    if obj.type == "MESH":
        obj.data.polygons.foreach_set("use_smooth", [True] * len(obj.data.polygons))


def new_material(name, color, rough=0.5, metal=0.0):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = color
    bsdf.inputs["Roughness"].default_value = rough
    bsdf.inputs["Metallic"].default_value = metal
    return mat


def add_text(name, body, size, mat, font, extrude=0.06):
    curve = bpy.data.curves.new(name, type="FONT")
    curve.body = body
    curve.size = size
    curve.font = font
    curve.align_x = "CENTER"
    curve.extrude = extrude
    curve.bevel_depth = 0.004
    obj = bpy.data.objects.new(name, curve)
    obj.data.materials.append(mat)
    bpy.context.collection.objects.link(obj)
    return obj


# ---------------------------------------------------------------- scene setup
def build_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.render.engine = "CYCLES"
    scene.cycles.device = "CPU"
    scene.cycles.samples = 24
    scene.cycles.use_adaptive_sampling = True
    scene.cycles.adaptive_threshold = 0.1
    scene.cycles.use_denoising = True
    scene.cycles.max_bounces = 4
    scene.render.use_persistent_data = True
    scene.render.resolution_x = 960
    scene.render.resolution_y = 540
    scene.render.fps = FPS
    scene.frame_start = FRAME_START
    scene.frame_end = FRAME_END
    scene.view_settings.view_transform = "AgX"
    scene.view_settings.exposure = -0.8
    try:
        scene.view_settings.look = "AgX - Punchy"
    except TypeError:
        pass

    world = bpy.data.worlds.new("World")
    scene.world = world
    world.use_nodes = True
    wnt = world.node_tree
    bg = wnt.nodes["Background"]
    bg.inputs["Strength"].default_value = 0.45
    wtex = wnt.nodes.new("ShaderNodeTexCoord")
    wsep = wnt.nodes.new("ShaderNodeSeparateXYZ")
    wnt.links.new(wtex.outputs["Generated"], wsep.inputs["Vector"])
    wmap = wnt.nodes.new("ShaderNodeMapRange")  # elevation -1..1 -> 0..1
    wmap.inputs["From Min"].default_value = -1.0
    wmap.inputs["From Max"].default_value = 1.0
    wnt.links.new(wsep.outputs["Y"], wmap.inputs["Value"])
    wramp = wnt.nodes.new("ShaderNodeValToRGB")
    wramp.color_ramp.elements[0].color = (0.35, 0.38, 0.43, 1)
    wramp.color_ramp.elements[1].color = (0.85, 0.9, 0.98, 1)
    wnt.links.new(wmap.outputs["Result"], wramp.inputs["Fac"])
    wnt.links.new(wramp.outputs["Color"], bg.inputs["Color"])

    font_bold = bpy.data.fonts.load(
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf")
    font_reg = bpy.data.fonts.load(
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf")

    # ---- pipe -----------------------------------------------------------
    depth = PIPE_Z1 - PIPE_Z0
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=96, radius=PIPE_RADIUS, depth=depth,
        end_fill_type="NOTHING", location=(0, 0, (PIPE_Z0 + PIPE_Z1) / 2))
    pipe = bpy.context.active_object
    pipe.name = "Pipe"
    solid = pipe.modifiers.new("Solid", "SOLIDIFY")
    solid.thickness = 0.1
    solid.offset = 1.0
    smooth_shade(pipe)

    pipe_mat = bpy.data.materials.new("PipeWall")
    pipe_mat.use_nodes = True
    nt = pipe_mat.node_tree
    bsdf = nt.nodes["Principled BSDF"]
    out = nt.nodes["Material Output"]

    texco = nt.nodes.new("ShaderNodeTexCoord")

    # aged concrete pipe wall: noisy grey-brown with joint grooves
    noise = nt.nodes.new("ShaderNodeTexNoise")
    noise.inputs["Scale"].default_value = 2.5
    noise.inputs["Detail"].default_value = 7.0
    nt.links.new(texco.outputs["Object"], noise.inputs["Vector"])
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.elements[0].color = (0.16, 0.14, 0.115, 1)
    ramp.color_ramp.elements[1].color = (0.34, 0.31, 0.27, 1)
    nt.links.new(noise.outputs["Fac"], ramp.inputs["Fac"])
    nt.links.new(ramp.outputs["Color"], bsdf.inputs["Base Color"])
    bsdf.inputs["Roughness"].default_value = 0.75

    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    nt.links.new(texco.outputs["Object"], sep.inputs["Vector"])
    wave = nt.nodes.new("ShaderNodeTexWave")  # pipe joints every ~4 m
    wave.inputs["Scale"].default_value = 0.25
    wave.inputs["Distortion"].default_value = 0.0
    wave.bands_direction = "Z"
    nt.links.new(texco.outputs["Object"], wave.inputs["Vector"])
    joint = nt.nodes.new("ShaderNodeMath")
    joint.operation = "POWER"
    joint.inputs[1].default_value = 30.0
    nt.links.new(wave.outputs["Fac"], joint.inputs[0])
    bump_mix = nt.nodes.new("ShaderNodeMath")
    bump_mix.operation = "MULTIPLY_ADD"
    nt.links.new(noise.outputs["Fac"], bump_mix.inputs[0])
    bump_mix.inputs[1].default_value = 0.3
    nt.links.new(joint.outputs[0], bump_mix.inputs[2])
    bump = nt.nodes.new("ShaderNodeBump")
    bump.inputs["Strength"].default_value = 0.35
    nt.links.new(bump_mix.outputs[0], bump.inputs["Height"])
    nt.links.new(bump.outputs["Normal"], bsdf.inputs["Normal"])

    # fresh resin liner: glossy epoxy applied behind the moving threshold
    resin = nt.nodes.new("ShaderNodeBsdfPrincipled")
    resin.inputs["Base Color"].default_value = RESIN
    resin.inputs["Roughness"].default_value = 0.13
    resin.inputs["Coat Weight"].default_value = 0.0

    gen_z = nt.nodes.new("ShaderNodeSeparateXYZ")
    nt.links.new(texco.outputs["Generated"], gen_z.inputs["Vector"])
    edge_noise = nt.nodes.new("ShaderNodeTexNoise")
    edge_noise.inputs["Scale"].default_value = 18.0
    nt.links.new(texco.outputs["Object"], edge_noise.inputs["Vector"])
    wobble = nt.nodes.new("ShaderNodeMath")
    wobble.operation = "MULTIPLY_ADD"
    nt.links.new(edge_noise.outputs["Fac"], wobble.inputs[0])
    wobble.inputs[1].default_value = 0.01
    nt.links.new(gen_z.outputs["Z"], wobble.inputs[2])

    thresh = nt.nodes.new("ShaderNodeValue")
    thresh.name = "ResinFront"
    thresh.label = "ResinFront"
    is_bare = nt.nodes.new("ShaderNodeMath")
    is_bare.operation = "GREATER_THAN"
    nt.links.new(wobble.outputs[0], is_bare.inputs[0])
    nt.links.new(thresh.outputs[0], is_bare.inputs[1])

    mix = nt.nodes.new("ShaderNodeMixShader")
    nt.links.new(is_bare.outputs[0], mix.inputs["Fac"])
    nt.links.new(resin.outputs[0], mix.inputs[1])      # fac 0 -> coated
    nt.links.new(bsdf.outputs[0], mix.inputs[2])       # fac 1 -> bare wall

    # thin blue UV-cure glow band right at the resin front
    band = nt.nodes.new("ShaderNodeMath")
    band.operation = "SUBTRACT"
    nt.links.new(gen_z.outputs["Z"], band.inputs[0])
    nt.links.new(thresh.outputs[0], band.inputs[1])
    band_abs = nt.nodes.new("ShaderNodeMath")
    band_abs.operation = "ABSOLUTE"
    nt.links.new(band.outputs[0], band_abs.inputs[0])
    band_in = nt.nodes.new("ShaderNodeMath")
    band_in.operation = "LESS_THAN"
    band_in.inputs[1].default_value = 0.0035
    nt.links.new(band_abs.outputs[0], band_in.inputs[0])
    glow = nt.nodes.new("ShaderNodeEmission")
    glow.inputs["Color"].default_value = (0.35, 0.55, 1.0, 1.0)
    glow.inputs["Strength"].default_value = 14.0
    mix2 = nt.nodes.new("ShaderNodeMixShader")
    nt.links.new(band_in.outputs[0], mix2.inputs["Fac"])
    nt.links.new(mix.outputs[0], mix2.inputs[1])
    nt.links.new(glow.outputs[0], mix2.inputs[2])
    nt.links.new(mix2.outputs[0], out.inputs["Surface"])
    pipe.data.materials.append(pipe_mat)
    resin_front_node = thresh

    # ---- wall + floor (studio exterior) ---------------------------------
    bpy.ops.mesh.primitive_cube_add(location=(0, 0, -0.05))
    wall = bpy.context.active_object
    wall.name = "Wall"
    wall.scale = (15, 15, 0.25)
    bpy.ops.mesh.primitive_cylinder_add(radius=PIPE_RADIUS + 0.16, depth=3,
                                        location=(0, 0, 0))
    cutter = bpy.context.active_object
    cutter.name = "WallCutter"
    cutter.hide_render = True
    boolmod = wall.modifiers.new("Hole", "BOOLEAN")
    boolmod.operation = "DIFFERENCE"
    boolmod.object = cutter
    wall.data.materials.append(new_material("WallMat", (0.78, 0.8, 0.82, 1), 0.6))

    bpy.ops.mesh.primitive_plane_add(size=80, location=(0, -1.5, 10),
                                     rotation=(math.radians(90), 0, 0))
    floor = bpy.context.active_object
    floor.name = "Floor"
    floor.data.materials.append(new_material("FloorMat", (0.72, 0.74, 0.76, 1), 0.45))

    # ---- applicator (resin packer with glowing cure ring) ---------------
    bpy.ops.mesh.primitive_torus_add(major_radius=0.7, minor_radius=0.06,
                                     major_segments=64, minor_segments=16)
    ring = bpy.context.active_object
    ring.name = "Applicator"
    smooth_shade(ring)
    ring_mat = bpy.data.materials.new("CureRing")
    ring_mat.use_nodes = True
    rn = ring_mat.node_tree.nodes["Principled BSDF"]
    rn.inputs["Emission Color"].default_value = (0.45, 0.62, 1.0, 1.0)
    rn.inputs["Emission Strength"].default_value = 3.0
    ring.data.materials.append(ring_mat)

    bpy.ops.mesh.primitive_cylinder_add(radius=0.18, depth=0.8, location=(0, 0, 0))
    hub = bpy.context.active_object
    hub.name = "ApplicatorHub"
    smooth_shade(hub)
    hub.data.materials.append(new_material("HubMat", (0.6, 0.6, 0.62, 1), 0.3, 1.0))
    hub.parent = ring

    cure_light = bpy.data.lights.new("CureLight", type="POINT")
    cure_light.energy = 30.0
    cure_light.color = (0.55, 0.68, 1.0)
    cure_light.shadow_soft_size = 0.3
    cure_obj = bpy.data.objects.new("CureLight", cure_light)
    bpy.context.collection.objects.link(cure_obj)
    cure_obj.parent = ring

    # ---- camera + crawler headlight --------------------------------------
    cam_data = bpy.data.cameras.new("Cam")
    cam_data.lens = 24.0
    cam_data.dof.use_dof = True
    cam = bpy.data.objects.new("Cam", cam_data)
    bpy.context.collection.objects.link(cam)
    scene.camera = cam

    cam.rotation_mode = "QUATERNION"

    head = bpy.data.lights.new("HeadLight", type="SPOT")
    head.energy = 50.0
    head.spot_size = math.radians(55)
    head.spot_blend = 0.4
    head.color = (1.0, 0.96, 0.9)
    head.shadow_soft_size = 0.08
    head_obj = bpy.data.objects.new("HeadLight", head)
    bpy.context.collection.objects.link(head_obj)
    head_obj.parent = cam
    head_obj.location = (0.0, 0.25, 0.1)

    # ---- exterior lighting -----------------------------------------------
    sun = bpy.data.lights.new("Sun", type="SUN")
    sun.energy = 2.5
    sun_obj = bpy.data.objects.new("Sun", sun)
    bpy.context.collection.objects.link(sun_obj)
    sun_obj.rotation_euler = (math.radians(55), math.radians(-12), math.radians(20))
    sun_obj.location = (4, 8, 10)

    softbox_mat = bpy.data.materials.new("Softbox")
    softbox_mat.use_nodes = True
    sb = softbox_mat.node_tree.nodes["Principled BSDF"]
    sb.inputs["Emission Color"].default_value = (1.0, 0.98, 0.94, 1.0)
    sb.inputs["Emission Strength"].default_value = 4.0
    for name, loc, rot in (
            ("SoftboxR", (9, 4.5, 4), (math.radians(70), math.radians(70), 0)),
            ("SoftboxL", (-7, 5.0, 9), (math.radians(60), math.radians(-50), 0))):
        bpy.ops.mesh.primitive_plane_add(size=4.5, location=loc, rotation=rot)
        panel = bpy.context.active_object
        panel.name = name
        panel.data.materials.append(softbox_mat)

    key = bpy.data.lights.new("KeyArea", type="AREA")
    key.energy = 900.0
    key.size = 6.0
    key_obj = bpy.data.objects.new("KeyArea", key)
    bpy.context.collection.objects.link(key_obj)
    key_obj.location = (4, 5, 9)
    key_obj.rotation_euler = (math.radians(-35), math.radians(25), 0)

    # ---- logo --------------------------------------------------------------
    logo = bpy.data.objects.new("LogoRoot", None)
    bpy.context.collection.objects.link(logo)

    navy = new_material("Navy", NAVY, 0.32, 0.7)
    amber = new_material("Amber", AMBER, 0.3, 0.4)

    bpy.ops.mesh.primitive_torus_add(major_radius=0.42, minor_radius=0.11,
                                     major_segments=64, minor_segments=24,
                                     location=(0, 0.85, 0))
    icon_ring = bpy.context.active_object
    icon_ring.name = "LogoRing"
    smooth_shade(icon_ring)
    icon_ring.data.materials.append(navy)
    icon_ring.parent = logo

    bpy.ops.mesh.primitive_cylinder_add(radius=0.115, depth=0.5,
                                        location=(0.58, 0.85, 0),
                                        rotation=(0, math.radians(90), 0))
    stub = bpy.context.active_object  # the "lateral" branch connection
    stub.name = "LogoStub"
    smooth_shade(stub)
    stub.data.materials.append(amber)
    stub.parent = logo

    t1 = add_text("LogoText1", "LATERAL", 0.46, navy, font_bold)
    t1.location = (0, -0.05, 0)
    t1.parent = logo
    t2 = add_text("LogoText2", "REPAIRS", 0.46, amber, font_bold)
    t2.location = (0, -0.52, 0)
    t2.parent = logo

    # ---- tagline -----------------------------------------------------------
    tag_mat = bpy.data.materials.new("TagMat")
    tag_mat.use_nodes = True
    tag_bsdf = tag_mat.node_tree.nodes["Principled BSDF"]
    tag_bsdf.inputs["Base Color"].default_value = AMBER
    tag_bsdf.inputs["Roughness"].default_value = 0.4
    tag_bsdf.inputs["Emission Color"].default_value = AMBER
    tag_bsdf.inputs["Emission Strength"].default_value = 0.35
    tag_bsdf.inputs["Alpha"].default_value = 0.0
    tagline = add_text("Tagline", "M A N U F A C T U R I N G   P E R F E C T I O N",
                       0.13, tag_mat, font_reg, extrude=0.01)
    tagline.location = (1.8, 0.95, 5.0)

    return scene, cam, ring, head_obj, logo, resin_front_node, tag_bsdf


def look_at_quat(eye, tgt):
    """Camera rotation looking from eye to tgt with +Y as world up."""
    fwd = (Vector(tgt) - Vector(eye)).normalized()
    right = fwd.cross(Vector((0.0, 1.0, 0.0))).normalized()
    up = right.cross(fwd)
    return Matrix((right, up, -fwd)).transposed().to_quaternion()


def bezier3(p0, c, p3, t):
    return tuple((1 - t) ** 2 * p0[i] + 2 * (1 - t) * t * c[i] + t ** 2 * p3[i]
                 for i in range(3))


# ---------------------------------------------------------------- animation
def animate(scene, cam, ring, head_obj, logo, resin_front, tag_bsdf):
    span = PIPE_Z1 - PIPE_Z0

    for f in range(FRAME_START, FRAME_END + 1):
        # --- camera position + aim ---
        if f <= 108:
            u = ease_io((f - 1) / 107.0)
            z = lerp(-36.0, -0.8, u)
            damp = 1.0 - clamp((z + 3.0) / 3.0, 0.0, 1.0)  # straighten near exit
            cx = 0.14 * math.sin(z * 0.45) * damp
            cy = (-0.08 + 0.10 * math.sin(z * 0.3 + 1.7)) * damp
            cam_pos = (cx, cy, z)
            tgt = (cx * 0.3, cy * 0.3, z + 4.8)
        elif f <= 145:
            t = ease_io((f - 108) / 37.0)
            cam_pos = bezier3((0, 0.02, -0.8), (3.2, 0.7, 4.0), (1.8, 1.85, 8.0), t)
            if f <= 130:
                # swing aim left/back to the pipe mouth as the camera arcs out
                tt = ease_io((f - 108) / 22.0)
                tgt = bezier3((0, 0, 4.0), (-4.0, 0.3, 2.0), (0, 0.4, 0.8), tt)
            else:
                tt = ease_io((f - 140) / 32.0)  # then follow the logo out
                tgt = (lerp(0, 1.8, tt), lerp(0.4, 1.85, tt), lerp(0.8, 5.0, tt))
        else:
            cam_pos = (1.8, 1.85, 8.0)
            if f <= 172:
                tt = ease_io((f - 140) / 32.0)
                tgt = (lerp(0, 1.8, tt), lerp(0.4, 1.85, tt), lerp(0.8, 5.0, tt))
            else:
                tgt = (1.8, 1.85, 5.0)

        cam.location = cam_pos
        cam.keyframe_insert("location", frame=f)
        cam.rotation_quaternion = look_at_quat(cam_pos, tgt)
        cam.keyframe_insert("rotation_quaternion", frame=f)

        # --- applicator + resin front ---
        z_app = min(cam_pos[2] + 3.4, -0.9) if f <= 108 else -0.9
        ring.location = (0, 0, z_app)
        ring.keyframe_insert("location", frame=f)
        resin_front.outputs[0].default_value = (z_app + 0.15 - PIPE_Z0) / span
        resin_front.outputs[0].keyframe_insert("default_value", frame=f)

        # --- crawler headlight fades once outside ---
        head_obj.data.energy = 50.0 * (1.0 - clamp((f - 108) / 15.0, 0.0, 1.0))
        head_obj.data.keyframe_insert("energy", frame=f)

        # --- logo launch ---
        if f < 138:
            logo.location = (0, 0, -100.0)
            logo.rotation_euler = (0, 0, 0)
            logo.scale = (1, 1, 1)
        else:
            t = clamp((f - 138) / 34.0, 0, 1)
            tz = ease_io(t)
            rise = ease_io((t - 0.40) / 0.60)
            logo.location = (1.8 * rise, 1.85 * rise, lerp(-3.0, 5.0, tz))
            logo.rotation_euler = (0, math.radians(360) * (1.0 - tz), 0)
            s = lerp(0.5, 0.85, ease_out_back(t))
            logo.scale = (s, s, s)
        logo.keyframe_insert("location", frame=f)
        logo.keyframe_insert("rotation_euler", frame=f)
        logo.keyframe_insert("scale", frame=f)

        # --- depth of field ---
        cam.data.dof.focus_distance = 3.5 if f <= 108 else lerp(3.5, 3.0,
                                            ease_io((f - 108) / 37.0))
        cam.data.dof.aperture_fstop = 12.0 if f <= 130 else lerp(
            12.0, 1.2, ease_io((f - 130) / 25.0))
        cam.data.dof.keyframe_insert("focus_distance", frame=f)
        cam.data.dof.keyframe_insert("aperture_fstop", frame=f)

        # --- tagline fade-in ---
        tag_bsdf.inputs["Alpha"].default_value = ease_io((f - 174) / 18.0)
        tag_bsdf.inputs["Alpha"].keyframe_insert("default_value", frame=f)


# ---------------------------------------------------------------- main
def main():
    scene, cam, ring, head_obj, logo, resin_front, tag_bsdf = build_scene()
    animate(scene, cam, ring, head_obj, logo, resin_front, tag_bsdf)

    bpy.ops.wm.save_as_mainfile(filepath="/tmp/lateral_repairs_promo.blend")

    args = sys.argv[1:]
    scene.render.image_settings.file_format = "PNG"
    if "--frame" in args:
        f = int(args[args.index("--frame") + 1])
        scene.frame_set(f)
        scene.render.filepath = f"{OUT_FRAMES}/frame_{f:04d}.png"
        bpy.ops.render.render(write_still=True)
    elif "--render" in args:
        i = args.index("--render")
        start, end = int(args[i + 1]), int(args[i + 2])
        for f in range(start, end + 1):
            scene.frame_set(f)
            scene.render.filepath = f"{OUT_FRAMES}/frame_{f:04d}.png"
            bpy.ops.render.render(write_still=True)


if __name__ == "__main__":
    main()
