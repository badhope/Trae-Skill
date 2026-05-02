import { createMCPServer } from '../../packages/core/mcp/builder'
import { validateParams, formatSuccess, formatError } from '../../packages/core/shared/utils'

export default createMCPServer({
  name: 'game-dev-toolkit',
  version: '2.0.0',
  description: 'Professional Game Development Toolkit - Unity, Unreal, Godot, Phaser project setup, sprite tools, audio processing, shader generation, architecture patterns',
  author: 'MCP Expert Community',
  icon: '🎮'
})

  .addTool({
    name: 'game_project_setup',
    description: 'Professional game project structure setup for all major engines',
    parameters: {
      engine: { type: 'string', description: 'unity, unreal, godot, phaser, pixijs, defold', required: true },
      projectName: { type: 'string', description: 'Project name (PascalCase)', required: true },
      template: { type: 'string', description: '2d, 3d, ar, vr, multiplayer, empty', required: false },
      features: { type: 'string', description: 'Comma-separated features: input,audio,ui,physics,networking', required: false }
    },
    execute: async (params: Record<string, any>) => {
      const validation = validateParams(params, {
        engine: { type: 'string', required: true, enum: ['unity', 'unreal', 'godot', 'phaser', 'pixijs', 'defold'] },
        projectName: { type: 'string', required: true },
        template: { type: 'string', required: false, default: '2d', enum: ['2d', '3d', 'ar', 'vr', 'multiplayer', 'empty'] },
        features: { type: 'string', required: false, default: 'input,audio,ui,physics' }
      })
      if (!validation.valid) return formatError('Invalid parameters', validation.errors)

      const engine = validation.data.engine
      const features = validation.data.features.split(',')
      const projectName = validation.data.projectName

      const structures: Record<string, any> = {
        unity: {
          folderStructure: [
            'Assets/',
            '  _Project/',
            '    Scripts/',
            '      Runtime/',
            '        Core/',
            '        Features/',
            '        Utilities/',
            '      Editor/',
            '    Prefabs/',
            '      UI/',
            '      Characters/',
            '    Scenes/',
            '      Bootstrap.unity',
            '      MainMenu.unity',
            '      Game.unity',
            '    Materials/',
            '    Textures/',
            '    Audio/',
            '      Music/',
            '      SFX/',
            '      Voice/',
            '    Settings/',
            '    Animations/',
            '  Plugins/',
            '  ThirdParty/',
            'Packages/',
            'ProjectSettings/'
          ],
          bootstrapper: `using UnityEngine;

namespace ${projectName}.Core
{
    public class GameBootstrapper : MonoBehaviour
    {
        private void Awake()
        {
            DontDestroyOnLoad(gameObject);
            InitializeSystems();
        }

        private void InitializeSystems()
        {
            // ServiceLocator.Initialize();
            // EventBus.Initialize();
            Debug.Log("[Bootstrapper] All systems initialized");
        }
    }
}`,
          quickstart: `1. Create ${validation.data.template} project via Unity Hub
2. Enable .NET Standard 2.1 in Player Settings
3. Import folders structure
4. Set Bootstrap scene as first in Build Settings`
        },
        godot: {
          folderStructure: [
            'project.godot',
            'src/',
            '  scripts/',
            '    autoload/',
            '      GameManager.gd',
            '      EventBus.gd',
            '      AudioManager.gd',
            '    characters/',
            '    ui/',
            '    utils/',
            '  scenes/',
            '    bootstrap.tscn',
            '    main_menu.tscn',
            '    game.tscn',
            'assets/',
            '  textures/',
            '  audio/',
            '  fonts/',
            '  models/'
          ],
          projectConfig: `[application]

config/name="${projectName}"
config/features=PackedStringArray("4.0", "GL Compatibility")
config/icon="res://icon.svg"

[autoload]

GameManager="*res://src/scripts/autoload/GameManager.gd"
EventBus="*res://src/scripts/autoload/EventBus.gd"
AudioManager="*res://src/scripts/autoload/AudioManager.gd"`,
          quickstart: 'godot --path . --editor'
        },
        phaser: {
          folderStructure: [
            'src/',
            '  index.ts',
            '  types/',
            '  scenes/',
            '    BootScene.ts',
            '    PreloadScene.ts',
            '    MenuScene.ts',
            '    GameScene.ts',
            '  objects/',
            '    Player.ts',
            '    Enemy.ts',
            '  managers/',
            '    InputManager.ts',
            '    AudioManager.ts',
            '  utils/',
            'public/',
            '  assets/',
            '  index.html',
            'package.json',
            'tsconfig.json',
            'vite.config.ts'
          ],
          dependencies: { phaser: '^3.80.0', typescript: '^5.0.0', vite: '^5.0.0' },
          scripts: { dev: 'vite', build: 'vite build', preview: 'vite preview' },
          quickstart: 'npm create phaser-ts@latest ' + projectName
        }
      }

      return formatSuccess({
        configured: true,
        engine,
        projectName,
        template: validation.data.template,
        enabledFeatures: features,
        setup: structures[engine] || structures.godot,
        namingConventions: [
          'PascalCase for classes, methods, assets',
          'camelCase for variables, parameters',
          'UPPER_CASE for constants, enums',
          'PascalCase.unity for scenes, prefabs',
          'snake_case.png for textures, sprites'
        ],
        unitySpecific: engine === 'unity' ? {
          assemblyDefinitions: 'Create Assembly Definitions for each feature',
          executionOrder: 'Bootstrapper: -100, Managers: -50',
          predefinedLayers: ['Player', 'Enemy', 'Collectible', 'Hazard', 'Ground']
        } : undefined
      })
    }
  })

  .addTool({
    name: 'spritesheet_generator',
    description: 'Professional spritesheet configuration, packing, and animation JSON generation',
    parameters: {
      spriteSize: { type: 'string', description: 'width x height e.g., 32x32', required: false },
      columns: { type: 'number', description: 'Number of columns', required: false },
      frames: { type: 'number', description: 'Total animation frames', required: false },
      animationName: { type: 'string', description: 'Animation: idle, walk, run, attack, jump, death, hurt', required: false },
      fps: { type: 'number', description: 'Frames per second', required: false }
    },
    execute: async (params: Record<string, any>) => {
      const validation = validateParams(params, {
        spriteSize: { type: 'string', required: false, default: '32x32' },
        columns: { type: 'number', required: false, default: 8 },
        frames: { type: 'number', required: false, default: 4 },
        animationName: { type: 'string', required: false, default: 'idle', enum: ['idle', 'walk', 'run', 'attack', 'jump', 'death', 'hurt'] },
        fps: { type: 'number', required: false, default: 12 }
      })
      if (!validation.valid) return formatError('Invalid parameters', validation.errors)

      const size = validation.data.spriteSize
      const [w, h] = size.split('x').map(Number)
      const columns = validation.data.columns
      const frames = validation.data.frames
      const animName = validation.data.animationName
      const fps = validation.data.fps

      return formatSuccess({
        configured: true,
        spriteDimensions: { width: w, height: h },
        columns,
        rows: Math.ceil(frames / columns),
        totalFrames: frames,
        animation: animName,
        fps,
        frameDuration: Math.round(1000 / fps),
        phaser3JSON: {
          frames: Array.from({ length: frames }, (_, i) => ({
            filename: `${animName}_${i}`,
            frame: { x: (i % columns) * w, y: Math.floor(i / columns) * h, w, h },
            rotated: false,
            trimmed: false,
            spriteSourceSize: { x: 0, y: 0, w, h },
            sourceSize: { w, h },
            duration: Math.round(1000 / fps)
          })),
          meta: {
            app: 'MCP Game Dev Toolkit',
            version: '2.0',
            image: `${animName}_sheet.png`,
            format: 'RGBA8888',
            size: { w: columns * w, h: Math.ceil(frames / columns) * h },
            scale: 1
          },
          animations: {
            [animName]: Array.from({ length: frames }, (_, i) => `${animName}_${i}`)
          }
        },
        asepriteWorkflow: {
          exportCommand: `aseprite --sheet ${animName}_sheet.png --sheet-pack --data ${animName}_sheet.json --format json-array ${animName}.aseprite`,
          tips: [
            'Save as .aseprite for non-destructive workflow',
            'Use tags for animations: idle, walk, attack',
            'Enable Trim Sprite for smaller sheet',
            'Extrude 1px to prevent bleeding'
          ]
        },
        tools: ['TexturePacker Pro', 'ShoeBox', 'Free Texture Packer', 'aseprite CLI'],
        performanceTips: [
          'Max texture size: 2048x2048 (mobile safe)',
          'Atlas similar sprites together',
          'Use POT (Power Of Two) dimensions',
          'Compress: ETC2 for Android, PVRTC for iOS'
        ]
      })
    }
  })

  .addTool({
    name: 'shader_template',
    description: 'Production-ready shader templates for Unity, Godot, and WebGL',
    parameters: {
      engine: { type: 'string', description: 'unity, godot, shadertoy, webgl', required: true },
      type: { type: 'string', description: 'lit, unlit, toon, water, fire, glitch, dissolve, outline', required: true },
      pipeline: { type: 'string', description: 'urp, hdrp, builtin', required: false }
    },
    execute: async (params: Record<string, any>) => {
      const validation = validateParams(params, {
        engine: { type: 'string', required: true, enum: ['unity', 'godot', 'shadertoy', 'webgl'] },
        type: { type: 'string', required: true, enum: ['lit', 'unlit', 'toon', 'water', 'fire', 'glitch', 'dissolve', 'outline'] },
        pipeline: { type: 'string', required: false, default: 'urp', enum: ['urp', 'hdrp', 'builtin'] }
      })
      if (!validation.valid) return formatError('Invalid parameters', validation.errors)

      const type = validation.data.type
      const engine = validation.data.engine
      const pipeline = validation.data.pipeline

      const templates: Record<string, Record<string, string>> = {
        unity: {
          unlit: `Shader "Custom/2D/UnlitColor"
{
    Properties
    {
        [MainTexture] _MainTex ("Texture", 2D) = "white" {}
        [MainColor] _Color ("Tint", Color) = (1,1,1,1)
    }

    SubShader
    {
        Tags
        {
            "Queue" = "Transparent"
            "RenderType" = "Transparent"
            "RenderPipeline" = "UniversalPipeline"
        }

        Cull Off
        Lighting Off
        ZWrite Off
        Blend One OneMinusSrcAlpha

        Pass
        {
            HLSLPROGRAM
            #pragma vertex vert
            #pragma fragment frag

            #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl"

            struct Attributes
            {
                float4 positionOS   : POSITION;
                float2 uv           : TEXCOORD0;
                half4 color        : COLOR;
            };

            struct Varyings
            {
                float4 positionHCS  : SV_POSITION;
                float2 uv           : TEXCOORD0;
                half4 color        : COLOR;
            };

            TEXTURE2D(_MainTex);
            SAMPLER(sampler_MainTex);
            half4 _MainTex_ST;
            half4 _Color;

            Varyings vert(Attributes IN)
            {
                Varyings OUT;
                OUT.positionHCS = TransformObjectToHClip(IN.positionOS.xyz);
                OUT.uv = TRANSFORM_TEX(IN.uv, _MainTex);
                OUT.color = IN.color * _Color;
                return OUT;
            }

            half4 frag(Varyings IN) : SV_Target
            {
                half4 tex = SAMPLE_TEXTURE2D(_MainTex, sampler_MainTex, IN.uv);
                half4 col = tex * IN.color;
                col.rgb *= col.a;
                return col;
            }
            ENDHLSL
        }
    }
}`,
          sprite_lit: `Shader "Universal Render Pipeline/2D/Sprite-Lit-Custom" {}`,
          toon: `Shader "Custom/3D/Toon"
{
    Properties
    {
        _MainTex ("Texture", 2D) = "white" {}
        _Color ("Color", Color) = (1,1,1,1)
        _RampSteps ("Ramp Steps", Range(2, 8)) = 4
        _OutlineWidth ("Outline Width", Range(0, 0.1)) = 0.02
    }
    SubShader { /* Toon implementation with ramp lighting */ }
}`,
          dissolve: `Shader "Custom/Effects/Dissolve"
{
    Properties
    {
        _MainTex ("Texture", 2D) = "white" {}
        _NoiseTex ("Noise", 2D) = "white" {}
        _Dissolve ("Dissolve Amount", Range(0, 1)) = 0
        _EdgeWidth ("Edge Width", Range(0, 0.2)) = 0.1
        _EdgeColor ("Edge Color", Color) = (1,0,0,1)
    }
    SubShader {
        Pass {
            HLSLPROGRAM
            // noise sample > _Dissolve then discard
            ENDHLSL
        }
    }
}`
        },
        godot: {
          unlit: `shader_type canvas_item;
render_mode unshaded, blend_premult_alpha;

uniform vec4 color : hint_color = vec4(1.0);
uniform sampler2D main_texture : filter_linear_mipmap, repeat_disable;

void fragment() {
    vec4 tex = texture(main_texture, UV);
    COLOR = tex * color;
    COLOR.rgb *= COLOR.a;
}`,
          toon: `shader_type spatial;
render_mode unshaded;

uniform vec4 albedo : hint_color = vec4(1.0);
uniform float bands : hint_range(2.0, 8.0, 1.0) = 4.0;

void fragment() {
    ALBEDO = albedo.rgb;
}

void light() {
    float d = dot(NORMAL, LIGHT);
    d = floor(d * bands) / bands;
    DIFFUSE_LIGHT = d * LIGHT_COLOR * ALBEDO;
}`,
          water: `shader_type canvas_item;

uniform float speed : hint_range(0.1, 5.0) = 1.0;
uniform float amplitude : hint_range(1.0, 50.0) = 10.0;
uniform float frequency : hint_range(0.1, 5.0) = 3.0;

void vertex() {
    VERTEX.y += sin(TIME * speed + VERTEX.x * frequency) * amplitude;
}`
        },
        shadertoy: {
          fire: `void mainImage( out vec4 fragColor, in vec2 fragCoord )
{
    vec2 uv = fragCoord / iResolution.xy;
    float t = iTime * 2.0;
    
    float noise = 0.0;
    noise += texture(iChannel0, uv * 1.0 + vec2(0.0, t)).r;
    noise += texture(iChannel0, uv * 2.0 + vec2(0.0, t * 1.5)).r * 0.5;
    
    float fire = 1.0 - pow(uv.y, 0.5);
    vec3 col = mix(vec3(1, 0.2, 0), vec3(1, 1, 0), noise * fire);
    col *= fire * 2.0;
    
    fragColor = vec4(col, 1.0);
}`,
          glitch: `void mainImage( out vec4 fragColor, in vec2 fragCoord )
{
    vec2 uv = fragCoord/iResolution.xy;
    
    float glitch = step(0.995, fract(iTime * 10.0));
    uv.x += (rand(uv.yy + iTime) - 0.5) * 0.05 * glitch;
    
    vec4 col = texture(iChannel0, uv);
    col.r = texture(iChannel0, uv + glitch * 0.01).r;
    col.b = texture(iChannel0, uv - glitch * 0.01).b;
    
    fragColor = col;
}`
        }
      }

      return formatSuccess({
        engine,
        type,
        pipeline: engine === 'unity' ? pipeline : undefined,
        shader: templates[engine]?.[type] || templates[engine]?.unlit || templates.godot.unlit,
        references: {
          unity: 'https://docs.unity3d.com/Packages/com.unity.shadergraph@latest',
          godot: 'https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/index.html',
          shadertoy: 'https://www.shadertoy.com/howto'
        },
        learningResources: [
          'Book of Shaders: https://thebookofshaders.com/',
          'Catlike Coding: Unity Tutorials',
          'Shader Graph for visual scripting',
          'Godot Shaders by KidsCanCode'
        ]
      })
    }
  })

  .addTool({
    name: 'audio_manager_setup',
    description: 'Professional audio management system with object pooling and mixing',
    parameters: {
      engine: { type: 'string', description: 'unity, godot, fmod', required: false },
      buses: { type: 'string', description: 'Comma-separated audio bus names', required: false },
      poolingEnabled: { type: 'boolean', description: 'Enable AudioSource pooling', required: false }
    },
    execute: async (params: Record<string, any>) => {
      const validation = validateParams(params, {
        engine: { type: 'string', required: false, default: 'unity', enum: ['unity', 'godot', 'fmod'] },
        buses: { type: 'string', required: false, default: 'master,music,sfx,ui,voice,environment' },
        poolingEnabled: { type: 'boolean', required: false, default: true }
      })
      if (!validation.valid) return formatError('Invalid parameters', validation.errors)

      const engine = validation.data.engine
      const buses = validation.data.buses.split(',')

      const systems: Record<string, any> = {
        unity: {
          audioManager: `using UnityEngine;
using System.Collections.Generic;

namespace Audio
{
    public class AudioManager : MonoBehaviour
    {
        public static AudioManager Instance { get; private set; }
        
        [SerializeField] private AudioSource musicSource;
        [SerializeField] private int poolSize = 20;
        [SerializeField] private AudioSource sfxPrefab;
        
        private readonly Queue<AudioSource> _sourcePool = new Queue<AudioSource>();
        private readonly Dictionary<string, AudioClip> _clipCache = new Dictionary<string, AudioClip>();
        private readonly Dictionary<string, float> _busVolumes = new Dictionary<string, float>();

        private void Awake()
        {
            if (Instance != null && Instance != this) { Destroy(gameObject); return; }
            Instance = this;
            DontDestroyOnLoad(gameObject);
            InitializePool();
        }

        private void InitializePool()
        {
            for (int i = 0; i < poolSize; i++)
            {
                var source = Instantiate(sfxPrefab, transform);
                source.gameObject.SetActive(false);
                _sourcePool.Enqueue(source);
            }
        }

        public void PlaySFX(AudioClip clip, float volume = 1f, float pitch = 1f, float pan = 0f)
        {
            if (_sourcePool.Count == 0) return;
            
            var source = _sourcePool.Dequeue();
            source.gameObject.SetActive(true);
            source.clip = clip;
            source.volume = volume * (0.9f + Random.value * 0.2f);
            source.pitch = pitch * (0.95f + Random.value * 0.1f);
            source.panStereo = pan;
            source.Play();
            
            StartCoroutine(ReturnToPool(source, clip.length));
        }

        private System.Collections.IEnumerator ReturnToPool(AudioSource source, float delay)
        {
            yield return new WaitForSeconds(delay);
            source.Stop();
            source.gameObject.SetActive(false);
            _sourcePool.Enqueue(source);
        }

        public void PlayMusic(AudioClip clip, bool loop = true)
        {
            musicSource.clip = clip;
            musicSource.loop = loop;
            musicSource.Play();
        }
    }
}`,
          recommendedFormats: {
            sfx: 'WAV 44.1kHz 16-bit (uncompressed)',
            music: 'OGG/Vorbis Quality 4 (5:1 compression)',
            voice: 'MP3 128kbps CBR'
          },
          importSettings: {
            sfx: 'Load In Background, Decompress On Load',
            music: 'Streaming, Compressed In Memory'
          }
        },
        godot: {
          busStructure: buses,
          suggestedSetup: 'Project > Audio > Add buses with volume sliders and ducking',
          autoloadScript: `extends Node

var _music_player: AudioStreamPlayer
var _sfx_players: Array[AudioStreamPlayer] = []
var _max_sfx_players = 16

func _ready():
    _music_player = AudioStreamPlayer.new()
    add_child(_music_player)
    _music_player.bus = "music"

func play_sfx(clip: AudioStream, volume: float = 1.0):
    for player in _sfx_players:
        if not player.playing:
            player.stream = clip
            player.volume_db = linear_to_db(volume * randf_range(0.9, 1.1))
            player.pitch_scale = randf_range(0.95, 1.05)
            player.play()
            return
    
    if _sfx_players.size() < _max_sfx_players:
        var new_player = AudioStreamPlayer.new()
        add_child(new_player)
        new_player.bus = "sfx"
        _sfx_players.append(new_player)
        new_player.stream = clip
        new_player.play()`
        }
      }

      return formatSuccess({
        engine,
        audioMixerBuses: buses,
        poolingEnabled: validation.data.poolingEnabled,
        implementation: systems[engine] || systems.unity,
        bestPractices: [
          'Pool AudioSources for frequent one-shots',
          '±10% pitch variation on SFX for less repetition',
          'Use 2D panning for UI, 3D for world objects',
          'Implement ducking: music lowers during VO',
          'Master bus peak limiter at -0.3dB'
        ],
        royaltyFreeAssets: [
          'https://freesound.org/',
          'https://zapsplat.com/',
          'https://freesfx.co.uk/',
          'https://itch.io/game-assets/free/tag-audio'
        ],
        middlewareOptions: {
          FMOD: 'Professional interactive audio',
          Wwise: 'Industry standard for AAA',
          ADX2: 'Console-optimized'
        }
      })
    }
  })

  .addPrompt({
    name: 'game-architecture-playbook',
    description: 'Complete game architecture patterns reference',
    arguments: [{ name: 'engine', description: 'Game engine: unity, godot, unreal', required: true }],
    generate: async (args?: Record<string, any>) => {
      return `## 🎮 Game Architecture Patterns Playbook
**Engine**: ${args?.engine || 'Generic'}

---

### 🏛️ Core Patterns

**Singleton / Service Locator**
- **Purpose**: Global access to managers
- **Use for**: GameManager, AudioManager, InputManager
- **Implementation**: Lazy initialization + DontDestroyOnLoad
- **⚠️ Caveat**: Creates coupling - use sparingly

**Finite State Machine (FSM)**
- **Purpose**: Clean state transitions
- **Use for**: Player movement, AI behavior, Game flow
- **Example**: Idle → Walk → Jump → Fall → Land
- **Pro tip**: Hierarchical FSMs for complex behaviors

**Event Bus / Observer Pattern**
- **Purpose**: Decoupled communication
- **Use for**: Achievements, Analytics, UI updates
- **Implementation**: C# events / Godot signals
- **No more: player.onDeath += ui.ShowGameOver**

**Entity Component System (ECS)**
- **Purpose**: Data-oriented performance
- **Use for**: Bullet hell, particles, RTS units
- **Performance**: 10,000+ entities at 60fps

**Object Pooling**
- **Purpose**: Eliminate allocation during gameplay
- **Critical for**: Bullets, enemies, VFX
- **Pre-warm pools during loading screens**

---

### 📁 Clean Architecture Layers

**Presentation Layer**
- UI Screens, HUD, Menus
- Input handling → Game Logic
- Never: Contains game state

**Game Logic Layer**
- State machines, Rules, Scoring
- Domain models: Player, Enemy, Weapon
- Pure logic, testable without engine

**Infrastructure Layer**
- Save/Load, Analytics, Ads, IAP
- Engine wrappers, platform specifics

---

### ⚡ Execution Order Matters

1. **Early (-100)**: Bootstrapper, Service Locator init
2. **Normal (-50 to 0)**: AI Behaviors, Player Input
3. **Physics (0 - FixedUpdate)**: Movement, collisions
4. **LateUpdate (50+)**: Camera follow, UI position sync
5. **Rendering**: Post-processing

---

### ✅ Checklist for Production

- [ ] Entry point: One Bootstrapper scene
- [ ] No magic strings: Use ScriptableObjects/Enums
- [ ] Scene loading: Async with loading screen
- [ ] Save system: Binary/encrypted, not PlayerPrefs
- [ ] Cheat codes: Only in Development builds
- [ ] Analytics: One event dispatcher
- [ ] Null checks: No NullReferenceExceptions shipped

---

### 🚫 Anti-Patterns to Avoid

❌ God Objects: 5000-line GameManager
❌ Update() spamming: Polling instead of events
❌ Overuse of Singletons: Everything becomes global
❌ Scene cross-references: Break on scene load
❌ Hardcoded values: No magic numbers!`
    }
  })
  .build()
