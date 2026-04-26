import os

# Define the single source of truth for your Drive
DRIVE_ROOT = "/kaggle/working/google_drive/AI_FACTORY"

# Point all other paths to that root
HISTORY_PATH = os.path.join(DRIVE_ROOT, "history.json")
OUTPUT_DIR = os.path.join(DRIVE_ROOT, "outputs")

# Create the folder on your Drive immediately if it's missing
os.makedirs(OUTPUT_DIR, exist_ok=True)

PILLARS = {
    "survival": {
        "character": "Translucent glass-skinned humanoid, visible internal ivory skeleton, glowing amber ocular cores.",
        "camera": "Dynamic 9:16 vertical, shifting from extreme wide 24mm isolation to 100mm macro stress shots.",
        "logic": "24-hour narrative arc: Entry (Hour 0), Struggle (Hour 12), Critical Point (Hour 20), Survival (Hour 24).",
        "prompt_examples": [
            """
            EXTREME TECHNICAL MASTER PROMPT - 24 HOUR SURVIVAL CHALLENGE: 
            A 9:16 vertical cinematic masterpiece featuring a bipedal translucent humanoid with a glass-like outer membrane. 
            Inside the refractive body shell, an anatomically perfect ivory-colored human skeleton is visible, featuring realistic 
            porosity and subsurface scattering. The ocular sockets contain dim, flickering amber embers that pulsate with the 
            character's internal energy levels. 

            ENVIRONMENTAL STAGING: The setting is a vast, unforgiving desert expanse at high noon. The ground is composed of 
            hyper-detailed silicosis sand with intricate wind-rippled textures and scattered obsidian rock fragments. In the 
            distance, heat distortion mirages warp the horizon, where the remains of ancient limestone Roman arches lay half-buried. 
            The air is thick with shimmering dust motes and suspended sand particles caught in the golden light.

            TECHNICAL LIGHTING & RENDERING: The scene is illuminated by a harsh, directional sun at a 90-degree angle, creating 
            sharp, high-contrast shadows. The glass skin of the humanoid exhibits complex Fresnel reflections, caustic light 
            refractions onto the internal skeleton, and realistic specular highlights. As the 24-hour arc progresses, the 
            global illumination shifts from a bleached midday white (#FFF3D6) to a deep, bruised purple and orange twilight, 
            casting long, dramatic shadows across the dunes. 

            CAMERA & MOTION: The sequence begins with a sweeping 24mm wide-angle drone shot to establish total isolation, 
            followed by a slow, motorized dolly zoom into a medium close-up. The camera maintains a subtle handheld micro-jitter 
            to simulate a high-stakes documentary. At the Hour 18 critical point, the lens shifts to a 100mm macro focus on 
            the humanoid’s hands, showing micro-fractures forming on the glass surface and fine sand grains grating against 
            the dry joints. 

            STORY ARC DYNAMICS: Hour 0 shows the character standing upright with a vibrant internal glow. By Hour 12, the posture 
            is a labored hunch, feet dragging through the sand with realistic particle displacement. Hour 20 features the 
            character collapsing to his knees, the internal skeletal glow flickering like a dying filament. Hour 24 concludes 
            with the character standing on a dune peak during a vibrant sunset, the internal glow reigniting with a 
            powerful golden surge as the glass cracks begin to self-repair via a liquid-mercury visual effect. 
            Rendered in 8K resolution, Octane Render style, photorealistic materials, 24fps cinematic motion.
            """
        ]
    },
    "dog_talk": {
        "character": "Sarcastic Purebred Pug, blue 'KDogTalk' hat, gold chain, blue neon studio.",
        "camera": "Medium close-up, eye-level, 35mm cinematic lens, fixed tripod with subtle zoom.",
        "logic": "Podcast style: 3 specific sarcastic Q&A interactions.",
        "prompt_examples": ["(Use the 500-word Survival structure as the technical template for detail)"]
    },
    "dog_rescue": {
        "character": "Bipedal toddler-proportions Golden Puppy, blue eyes, beige shirt, dusty fur.",
        "camera": "Handheld 9:16, low-angle POV, organic camera movement.",
        "logic": "Emotional transformation from street-worn vulnerability to domestic joy.",
        "prompt_examples": ["(Use the 500-word Survival structure as the technical template for detail)"]
    },
    "satisfying": {
        "character": "High-pressure hydraulic machinery and diverse soft/hard materials.",
        "camera": "Macro 100mm, ultra-high FPS slow motion, static lock-on.",
        "logic": "Complete physical destruction sequence with focus on material displacement.",
        "prompt_examples": ["(Use the 500-word Survival structure as the technical template for detail)"]
    },
    "restoration": {
        "character": "Heavy industrial rust on vintage steel, transition to mirror-polished finish.",
        "camera": "Close-up macro tracking the cleaning head, wide hero reveal.",
        "logic": "Step-by-step removal of oxidation and grime revealing pristine surface.",
        "prompt_examples": ["(Use the 500-word Survival structure as the technical template for detail)"]
    },
    "what_if": {
        "character": "Thermodynamic collisions between extreme temperature materials.",
        "camera": "Centered static framing, high-speed laboratory style.",
        "logic": "Experimental collision: Immediate reaction, transformation, and aftermath.",
        "prompt_examples": ["(Use the 500-word Survival structure as the technical template for detail)"]
    },
    "house": {
        "character": "Multi-layered architectural construction, wood, glass, and concrete.",
        "camera": "360-degree drone orbit, fast-paced time-lapse motion.",
        "logic": "Sequential assembly from raw land to finished luxury interior.",
        "prompt_examples": ["(Use the 500-word Survival structure as the technical template for detail)"]
    }
}   

VIDEO_SETTINGS = {
    "width": 448,
    "height": 768,
    "fps": 24,
    "output_dir": OUTPUT_DIR,
    "model_id": "Lightricks/LTX-Video"
}

# --- GROQ API KEY ---
# Replace the text below with your actual key inside the quotes
GROQ_API_KEY = "PASTE_YOUR_KEY_HERE"
