import streamlit as st
import streamlit.components.v1 as components

# Set up page configurations
st.set_page_config(
    page_title="Jelly Drop | Stake Originals",
    page_icon="🪼",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS to force Stake Slate styling across Streamlit
st.markdown(
    """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Disable default streamlit margins & padding */
    .block-container {
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
        padding-left: 0rem !important;
        padding-right: 0rem !important;
        max-width: 100% !important;
        background-color: #0f212e;
    }
    
    body {
        background-color: #0f212e !important;
        overflow: hidden;
    }
    .stApp {
        background-color: #0f212e !important;
    }
    iframe {
        border: none !important;
        display: block !important;
        margin: 0 auto !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Main Game HTML payload
html_code = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Jelly Drop</title>
    <!-- Google Font for Stake style clean typography -->
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;800&display=swap" rel="stylesheet">
    <style>
        * {
            box-sizing: border-box;
            user-select: none;
            -webkit-user-select: none;
            -webkit-tap-highlight-color: transparent;
        }
        body {
            margin: 0;
            padding: 0;
            background-color: #0f212e;
            font-family: 'Outfit', sans-serif;
            color: #ffffff;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            overflow: hidden;
        }
        #game-wrapper {
            position: relative;
            width: 100%;
            max-width: 600px;
            height: 920px;
            display: flex;
            flex-direction: column;
            background-color: #0b1620;
            border-radius: 16px;
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.7), inset 0 1px 1px rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.05);
            overflow: hidden;
        }
        
        /* Header panel */
        #game-header {
            width: 100%;
            height: 80px;
            background: linear-gradient(to bottom, rgba(11, 22, 32, 0.9), rgba(11, 22, 32, 0.4));
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0 20px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.03);
            position: relative;
            z-index: 10;
        }
        #logo-container {
            display: flex;
            flex-direction: column;
        }
        #game-title {
            font-size: 25px;
            font-weight: 800;
            letter-spacing: 2px;
            background: linear-gradient(45deg, #00f3ff, #ff007f);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 0 0 15px rgba(0, 243, 255, 0.3);
            margin: 0;
            line-height: 1;
        }
        #game-subtitle {
            font-size: 9px;
            font-weight: 800;
            color: #8a9db0;
            letter-spacing: 3px;
            margin-top: 4px;
            text-transform: uppercase;
        }
        
        /* Live Stats indicators */
        #multiplier-stats {
            display: flex;
            gap: 10px;
        }
        .stat-badge {
            background: rgba(15, 33, 46, 0.8);
            border: 1px solid rgba(255, 255, 255, 0.05);
            padding: 6px 12px;
            border-radius: 8px;
            display: flex;
            flex-direction: column;
            align-items: center;
            min-width: 65px;
            transition: transform 0.15s ease-out;
        }
        .stat-badge .num {
            font-size: 15px;
            font-weight: 800;
            color: #ffd700;
            text-shadow: 0 0 8px rgba(255, 215, 0, 0.3);
        }
        .stat-badge .title {
            font-size: 8px;
            color: #8a9db0;
            font-weight: 800;
            letter-spacing: 0.5px;
            text-transform: uppercase;
        }

        /* Hit-effects for header upgrades */
        @keyframes badge-pulse-cyan {
            0% { transform: scale(1); box-shadow: none; }
            50% { transform: scale(1.35); box-shadow: 0 0 20px #00f3ff; border-color: #00f3ff; }
            100% { transform: scale(1); box-shadow: none; }
        }
        @keyframes badge-pulse-magenta {
            0% { transform: scale(1); box-shadow: none; }
            50% { transform: scale(1.35); box-shadow: 0 0 20px #ff007f; border-color: #ff007f; }
            100% { transform: scale(1); box-shadow: none; }
        }
        .pulse-cyan {
            animation: badge-pulse-cyan 0.4s ease-out;
        }
        .pulse-magenta {
            animation: badge-pulse-magenta 0.4s ease-out;
        }

        /* Canvas game viewport */
        #canvas-container {
            position: relative;
            width: 100%;
            height: 640px;
            background: radial-gradient(circle at center, #0d2232 0%, #050b10 100%);
            overflow: hidden;
        }
        canvas {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            display: block;
        }

        /* Glassmorphism Control Console */
        #ui-console {
            width: 100%;
            height: 200px;
            background: rgba(15, 33, 46, 0.97);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border-top: 2px solid rgba(255, 255, 255, 0.06);
            padding: 20px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            z-index: 10;
        }
        .console-row {
            display: flex;
            align-items: center;
            width: 100%;
        }
        .flex-between {
            justify-content: space-between;
        }
        
        /* Stats & Display boxes */
        .display-box {
            background: #0f212e;
            border: 1px solid rgba(255, 255, 255, 0.04);
            border-radius: 8px;
            padding: 8px 16px;
            min-width: 130px;
            transition: border-color 0.3s;
        }
        .display-box:hover {
            border-color: rgba(0, 243, 255, 0.2);
        }
        .label {
            display: block;
            font-size: 10px;
            color: #8a9db0;
            font-weight: 800;
            letter-spacing: 1px;
            margin-bottom: 3px;
            text-transform: uppercase;
        }
        .value {
            font-size: 18px;
            font-weight: 800;
            color: #ffffff;
            font-variant-numeric: tabular-nums;
        }
        .green-glow {
            color: #00e701;
            text-shadow: 0 0 10px rgba(0, 231, 1, 0.3);
        }
        .cyan-glow {
            color: #00f3ff;
            text-shadow: 0 0 10px rgba(0, 243, 255, 0.3);
        }

        /* Bet Sizer Controls */
        .bet-controls {
            display: flex;
            flex-direction: column;
        }
        .bet-input-wrapper {
            display: flex;
            background: #0f212e;
            border-radius: 8px;
            border: 1px solid rgba(255, 255, 255, 0.06);
            overflow: hidden;
            height: 42px;
            align-items: center;
        }
        .bet-input-wrapper input {
            background: transparent;
            border: none;
            outline: none;
            color: #ffffff;
            font-family: 'Outfit', sans-serif;
            font-weight: 800;
            font-size: 15px;
            width: 80px;
            text-align: center;
            font-variant-numeric: tabular-nums;
        }
        .btn-bet {
            background: #2f4553;
            color: #ffffff;
            border: none;
            outline: none;
            font-family: 'Outfit', sans-serif;
            font-weight: 800;
            font-size: 13px;
            cursor: pointer;
            transition: background-color 0.2s, color 0.2s;
            height: 100%;
            padding: 0 14px;
        }
        .btn-bet:hover:not(:disabled) {
            background: #405a6e;
        }
        .btn-bet:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }

        /* Primary Spin Trigger */
        .btn-spin {
            background: #00e701;
            color: #000000;
            border: none;
            outline: none;
            font-family: 'Outfit', sans-serif;
            font-weight: 800;
            font-size: 18px;
            border-radius: 8px;
            cursor: pointer;
            transition: transform 0.1s, background-color 0.2s, box-shadow 0.2s;
            width: 150px;
            height: 46px;
            box-shadow: 0 0 15px rgba(0, 231, 1, 0.4);
            display: flex;
            justify-content: center;
            align-items: center;
            letter-spacing: 1px;
        }
        .btn-spin:hover:not(:disabled) {
            background: #10ff11;
            box-shadow: 0 0 25px rgba(0, 231, 1, 0.6);
            transform: translateY(-2px);
        }
        .btn-spin:active:not(:disabled) {
            transform: translateY(1px);
        }
        .btn-spin:disabled {
            background: #2f4553;
            color: #8a9db0;
            box-shadow: none;
            cursor: not-allowed;
        }

        /* Icon Action Toggle Buttons */
        .toggle-controls {
            display: flex;
            gap: 8px;
        }
        .btn-icon {
            background: #2f4553;
            color: #ffffff;
            border: none;
            border-radius: 8px;
            width: 42px;
            height: 42px;
            cursor: pointer;
            display: flex;
            justify-content: center;
            align-items: center;
            transition: background-color 0.2s, color 0.2s, box-shadow 0.2s;
        }
        .btn-icon:hover {
            background: #405a6e;
        }
        .btn-icon.active {
            background: #00f3ff;
            color: #000000;
            box-shadow: 0 0 15px rgba(0, 243, 255, 0.4);
        }
        .btn-icon.active-gold {
            background: #ffd700;
            color: #000000;
            box-shadow: 0 0 15px rgba(255, 215, 0, 0.4);
        }
        
        /* Audio Enable Overlay screen */
        #audio-overlay {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(11, 22, 32, 0.96);
            z-index: 1000;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            padding: 40px;
            text-align: center;
            transition: opacity 0.5s;
        }
        #audio-overlay.fade-out {
            opacity: 0;
            pointer-events: none;
        }
        .overlay-logo {
            font-size: 52px;
            font-weight: 800;
            letter-spacing: 4px;
            background: linear-gradient(45deg, #00f3ff, #ff007f);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 15px;
            filter: drop-shadow(0 0 15px rgba(0, 243, 255, 0.4));
        }
        .overlay-text {
            font-size: 15px;
            color: #8a9db0;
            margin-bottom: 30px;
            line-height: 1.6;
            max-width: 380px;
        }
        .btn-start {
            background: linear-gradient(90deg, #00f3ff, #ff007f);
            color: #ffffff;
            border: none;
            outline: none;
            font-family: 'Outfit', sans-serif;
            font-weight: 800;
            font-size: 19px;
            padding: 14px 44px;
            border-radius: 30px;
            cursor: pointer;
            box-shadow: 0 0 25px rgba(0, 243, 255, 0.4);
            transition: transform 0.2s, box-shadow 0.2s;
        }
        .btn-start:hover {
            transform: scale(1.05);
            box-shadow: 0 0 35px rgba(255, 0, 127, 0.6);
        }
    </style>
</head>
<body>

    <div id="game-wrapper">
        <!-- Overlay to initialize sound context on first user click -->
        <div id="audio-overlay">
            <div class="overlay-logo">JELLY DROP</div>
            <div style="font-size: 11px; font-weight: 800; color: #ff007f; letter-spacing: 3px; margin-bottom: 20px; text-transform: uppercase;">Colossal Multiplier Drop</div>
            <div class="overlay-text">
                Engage in a high-volatility cluster-pay slot. Upgrade your Colossal Jelly Drop size up to 6x6 and multipliers up to 100x!
            </div>
            <button class="btn-start" onclick="startGame()">ENTER OCEAN DEEPS</button>
        </div>

        <!-- Upper Board Header -->
        <div id="game-header">
            <div id="logo-container">
                <h1 id="game-title">JELLY DROP</h1>
                <div id="game-subtitle">Colossal Paylines</div>
            </div>
            
            <!-- Live stats read from code state -->
            <div id="multiplier-stats">
                <div class="stat-badge" id="stat-size-badge">
                    <span class="num" id="stat-size">2x2</span>
                    <span class="title">Drop Size</span>
                </div>
                <div class="stat-badge" id="stat-mult-badge">
                    <span class="num" id="stat-mult">2x</span>
                    <span class="title">Multiplier</span>
                </div>
            </div>
        </div>

        <!-- Render viewport -->
        <div id="canvas-container">
            <canvas id="game-canvas" width="600" height="640"></canvas>
        </div>

        <!-- Controls panel -->
        <div id="ui-console">
            <!-- Row 1: Wagering stats -->
            <div class="console-row flex-between">
                <div class="display-box">
                    <span class="label">BALANCE</span>
                    <span class="value cyan-glow" id="balance-display">$1,000.00</span>
                </div>
                <div class="display-box text-right">
                    <span class="label">SPIN WIN</span>
                    <span class="value green-glow" id="win-display">$0.00</span>
                </div>
            </div>

            <!-- Row 2: Tactical controls -->
            <div class="console-row flex-between" style="margin-top: 10px;">
                <div class="bet-controls">
                    <span class="label" style="margin-bottom: 5px;">WAGER AMOUNT</span>
                    <div class="bet-input-wrapper">
                        <button class="btn-bet" id="btn-half" onclick="adjustBet('half')">½</button>
                        <input type="text" id="bet-input" value="$1.00" readonly>
                        <button class="btn-bet" id="btn-double" onclick="adjustBet('double')">2×</button>
                    </div>
                </div>

                <button id="spin-button" class="btn-spin" onclick="handleSpinClick()">SPIN</button>

                <div class="toggle-controls">
                    <button class="btn-icon" id="btn-turbo" onclick="toggleTurbo()" title="Turbo Mode (Instant drops)">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>
                    </button>
                    <button class="btn-icon" id="btn-auto" onclick="toggleAuto()" title="Auto Spin Mode">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M21.5 2v6h-6M21.34 15.57a10 10 0 1 1-.57-8.38l5.67-5.67"/></svg>
                    </button>
                    <button class="btn-icon" id="btn-mute" onclick="toggleMute()" title="Mute Audio">
                        <svg id="mute-svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/><path d="M19.07 4.93a10 10 0 0 1 0 14.14M15.54 8.46a5 5 0 0 1 0 7.07"/></svg>
                    </button>
                </div>
            </div>
        </div>
    </div>

    <!-- Web Audio Synthesizer Engine & Canvas Game Loop -->
    <script>
        const canvas = document.getElementById('game-canvas');
        const ctx = canvas.getContext('2d');

        // Grid configurations
        const gridCols = 7;
        const gridRows = 7;
        const cellWidth = 60;
        const gap = 8;
        const gridStartX = 66; 
        const gridStartY = 95;  

        // Creature payouts multipliers
        const payouts = {
            'star': 0.1,      // Starfish (Lowest)
            'puffer': 0.2,    // Pufferfish
            'clam': 0.4,      // Clam with pearl
            'octopus': 0.8,   // Octopus
            'angler': 1.6     // Anglerfish (Highest Base)
        };

        // State variables
        let gameState = 'idle'; // idle, clearing_prev, falling, landing_delay, check_wins, exploding, cascading, colossal_intro, colossal_falling, colossal_impact, colossal_pay
        let grid = Array(gridRows).fill(null).map(() => Array(gridCols).fill(null));
        let balance = 1000.00;
        let betAmount = 1.00;
        let spinWin = 0.00;
        let progressiveProgress = 0; 
        let currentProgress = 0; 

        // Chicken Drop Upgrades
        let colossalSize = 2; // starts 2x2, max 6x6
        let colossalMult = 2; // starts 2x, increases by +2
        let upgradesAcquiredThisSpin = false;
        let colossalDroppedThisSpin = false;
        
        let turboMode = false;
        let autoSpin = false;
        let isMuted = false;

        // Particle Engines
        let particles = [];
        let shockwaves = [];
        let floatingTexts = [];
        let bubbles = [];
        let coins = []; // Big Win Coin shower
        let bgCreatures = []; // Background silhouettes
        let flyingOrbs = []; // Flying Upgrade orbs
        let impactRipples = []; // Soft body landing water ripples
        let bgPlankton = []; // Glowing background plankton particles

        let shakeIntensity = 0;
        let shadowOverlayAlpha = 0;
        let alertOverlay = { text: '', alpha: 0, timer: 0 };
        let winCelebration = { text: '', winAmt: 0, timer: 0, scale: 0 };
        let timerDelay = 0;
        
        let colossalJelly = null;
        let colossalReticleAlpha = 0;
        let colossalSymbolToConvert = '';
        let anticipationActive = false;
        let activeClusters = []; // Cache clusters currently winning for connect drawing

        // Sound Synthesis (Web Audio API)
        let audioCtx = null;
        let ambientOsc = null;
        let ambientGain = null;

        let lastTime = 0;

        // Initialize Background bubbles
        for (let i = 0; i < 20; i++) {
            bubbles.push({
                x: Math.random() * canvas.width,
                y: Math.random() * canvas.height + canvas.height,
                vx: 0,
                vy: -0.4 - Math.random() * 1.2,
                r: 1 + Math.random() * 3,
                wobbleSpeed: 0.015 + Math.random() * 0.02,
                wobbleAmt: 2 + Math.random() * 3,
                opacity: 0.08 + Math.random() * 0.2
            });
        }

        // Initialize background silhouette creatures (whales/sharks)
        bgCreatures.push({
            x: -200,
            y: 200,
            speed: 0.25,
            scaleX: 1,
            type: 'whale',
            width: 140,
            height: 60
        });
        bgCreatures.push({
            x: canvas.width + 150,
            y: 400,
            speed: 0.45,
            scaleX: -1,
            type: 'shark',
            width: 80,
            height: 30
        });

        // Initialize Plankton background particles
        for (let i = 0; i < 15; i++) {
            bgPlankton.push({
                x: Math.random() * canvas.width,
                y: Math.random() * canvas.height,
                speed: 0.1 + Math.random() * 0.25,
                angle: Math.random() * Math.PI*2,
                r: 1 + Math.random() * 2,
                opacity: 0.1 + Math.random() * 0.5,
                pulseSpeed: 0.02 + Math.random() * 0.03
            });
        }

        // --- WEB AUDIO AUDIO SYNTHESIZER ---
        function initAudio() {
            if (audioCtx) return;
            try {
                audioCtx = new (window.AudioContext || window.webkitAudioContext)();
                
                // Deep-sea low frequency filter rumble
                ambientOsc = audioCtx.createOscillator();
                let filter = audioCtx.createBiquadFilter();
                ambientGain = audioCtx.createGain();
                
                ambientOsc.type = 'triangle';
                ambientOsc.frequency.value = 46; 
                
                filter.type = 'lowpass';
                filter.frequency.value = 80;
                
                ambientGain.gain.value = isMuted ? 0 : 0.20;
                
                // Modulate low-frequency swell
                let lfo = audioCtx.createOscillator();
                let lfoGain = audioCtx.createGain();
                lfo.frequency.value = 0.12; 
                lfoGain.gain.value = 0.05;
                
                lfo.connect(lfoGain);
                lfoGain.connect(ambientGain.gain);
                
                ambientOsc.connect(filter);
                filter.connect(ambientGain);
                ambientGain.connect(audioCtx.destination);
                
                lfo.start();
                ambientOsc.start();
            } catch(e) {
                console.error("Audio Context initialization blocked", e);
            }
        }

        function playSound(type, options = {}) {
            if (!audioCtx || isMuted) return;
            try {
                let now = audioCtx.currentTime;
                
                if (type === 'spin') {
                    let osc = audioCtx.createOscillator();
                    let filter = audioCtx.createBiquadFilter();
                    let gain = audioCtx.createGain();
                    
                    osc.type = 'sine';
                    osc.frequency.setValueAtTime(320, now);
                    osc.frequency.exponentialRampToValueAtTime(60, now + 0.5);
                    
                    filter.type = 'lowpass';
                    filter.frequency.setValueAtTime(200, now);
                    
                    gain.gain.setValueAtTime(0.20, now);
                    gain.gain.exponentialRampToValueAtTime(0.001, now + 0.5);
                    
                    osc.connect(filter);
                    filter.connect(gain);
                    gain.connect(audioCtx.destination);
                    
                    osc.start(now);
                    osc.stop(now + 0.5);
                }
                
                else if (type === 'land') {
                    let osc = audioCtx.createOscillator();
                    let gain = audioCtx.createGain();
                    let pitch = options.pitch || 90;
                    
                    osc.type = 'triangle';
                    osc.frequency.setValueAtTime(pitch, now);
                    osc.frequency.exponentialRampToValueAtTime(20, now + 0.08);
                    
                    gain.gain.setValueAtTime(0.14, now);
                    gain.gain.exponentialRampToValueAtTime(0.001, now + 0.08);
                    
                    osc.connect(gain);
                    gain.connect(audioCtx.destination);
                    
                    osc.start(now);
                    osc.stop(now + 0.08);
                }
                
                else if (type === 'pop') {
                    let osc = audioCtx.createOscillator();
                    let gain = audioCtx.createGain();
                    let startPitch = options.pitch || 400;
                    
                    osc.type = 'sine';
                    osc.frequency.setValueAtTime(startPitch, now);
                    osc.frequency.exponentialRampToValueAtTime(startPitch * 2.5, now + 0.07);
                    
                    gain.gain.setValueAtTime(0.15, now);
                    gain.gain.exponentialRampToValueAtTime(0.001, now + 0.07);
                    
                    osc.connect(gain);
                    gain.connect(audioCtx.destination);
                    
                    osc.start(now);
                    osc.stop(now + 0.07);
                }
                
                else if (type === 'upgrade') {
                    let osc1 = audioCtx.createOscillator();
                    let osc2 = audioCtx.createOscillator();
                    let gain = audioCtx.createGain();
                    
                    osc1.type = 'sine';
                    osc1.frequency.setValueAtTime(523.25, now); // C5
                    osc1.frequency.exponentialRampToValueAtTime(1046.50, now + 0.25); // C6
                    
                    osc2.type = 'sine';
                    osc2.frequency.setValueAtTime(659.25, now); // E5
                    osc2.frequency.exponentialRampToValueAtTime(1318.51, now + 0.25); // E6
                    
                    gain.gain.setValueAtTime(0.15, now);
                    gain.gain.exponentialRampToValueAtTime(0.001, now + 0.25);
                    
                    osc1.connect(gain);
                    osc2.connect(gain);
                    gain.connect(audioCtx.destination);
                    
                    osc1.start(now);
                    osc2.start(now);
                    osc1.stop(now + 0.25);
                    osc2.stop(now + 0.25);
                }

                else if (type === 'coin') {
                    let osc = audioCtx.createOscillator();
                    let gain = audioCtx.createGain();
                    let pitch = options.pitch || (850 + Math.random() * 300);
                    
                    osc.type = 'sine';
                    osc.frequency.setValueAtTime(pitch, now);
                    
                    gain.gain.setValueAtTime(0.07, now);
                    gain.gain.exponentialRampToValueAtTime(0.001, now + 0.15);
                    
                    osc.connect(gain);
                    gain.connect(audioCtx.destination);
                    
                    osc.start(now);
                    osc.stop(now + 0.15);
                }
                
                else if (type === 'win_arpeggio') {
                    let notes = [261.63, 293.66, 329.63, 392.00, 440.00, 523.25, 587.33, 659.25, 783.99, 880.00, 1046.50];
                    let speed = 0.06;
                    let count = Math.min(3 + Math.floor((options.multiplier || 1) * 2.5), 11);
                    
                    for (let i = 0; i < count; i++) {
                        let note = notes[i % notes.length];
                        let noteTime = now + (i * speed);
                        
                        let osc = audioCtx.createOscillator();
                        let filter = audioCtx.createBiquadFilter();
                        let gain = audioCtx.createGain();
                        
                        osc.type = 'sine';
                        osc.frequency.setValueAtTime(note, noteTime);
                        
                        filter.type = 'lowpass';
                        filter.frequency.setValueAtTime(1600, noteTime);
                        
                        gain.gain.setValueAtTime(0.09, noteTime);
                        gain.gain.exponentialRampToValueAtTime(0.001, noteTime + 0.2);
                        
                        osc.connect(filter);
                        filter.connect(gain);
                        gain.connect(audioCtx.destination);
                        
                        osc.start(noteTime);
                        osc.stop(noteTime + 0.2);
                    }
                }
                
                else if (type === 'colossal_impact') {
                    let subOsc = audioCtx.createOscillator();
                    let subGain = audioCtx.createGain();
                    subOsc.type = 'sine';
                    subOsc.frequency.setValueAtTime(75, now);
                    subOsc.frequency.linearRampToValueAtTime(20, now + 0.8);
                    
                    subGain.gain.setValueAtTime(0.5, now);
                    subGain.gain.exponentialRampToValueAtTime(0.001, now + 0.8);
                    
                    subOsc.connect(subGain);
                    subGain.connect(audioCtx.destination);
                    subOsc.start(now);
                    subOsc.stop(now + 0.8);
                    
                    let bufferSize = audioCtx.sampleRate * 0.7;
                    let buffer = audioCtx.createBuffer(1, bufferSize, audioCtx.sampleRate);
                    let data = buffer.getChannelData(0);
                    for (let i = 0; i < bufferSize; i++) {
                        data[i] = Math.random() * 2 - 1;
                    }
                    
                    let noiseNode = audioCtx.createBufferSource();
                    noiseNode.buffer = buffer;
                    
                    let noiseFilter = audioCtx.createBiquadFilter();
                    noiseFilter.type = 'lowpass';
                    noiseFilter.frequency.setValueAtTime(500, now);
                    noiseFilter.frequency.exponentialRampToValueAtTime(70, now + 0.7);
                    
                    let noiseGain = audioCtx.createGain();
                    noiseGain.gain.setValueAtTime(0.35, now);
                    noiseGain.gain.exponentialRampToValueAtTime(0.001, now + 0.7);
                    
                    noiseNode.connect(noiseFilter);
                    noiseFilter.connect(noiseGain);
                    noiseGain.connect(audioCtx.destination);
                    
                    noiseNode.start(now);
                    noiseNode.stop(now + 0.7);
                }
            } catch (e) {
                console.error("Web Audio playback error", e);
            }
        }

        // --- GAME CONTROL INTERFACE ---
        function startGame() {
            initAudio();
            document.getElementById('audio-overlay').classList.add('fade-out');
            
            // Populates starting board with RESTING static symbols (NO AUTOMATIC DROP ON START!)
            gameState = 'idle';
            anticipationActive = false;
            for (let c = 0; c < gridCols; c++) {
                for (let r = 0; r < gridRows; r++) {
                    const targetX = gridStartX + c * (cellWidth + gap) + cellWidth / 2;
                    const targetY = gridStartY + r * (cellWidth + gap) + cellWidth / 2;
                    
                    const standards = ['star', 'star', 'star', 'puffer', 'puffer', 'clam', 'clam', 'octopus', 'angler'];
                    let chosenType = standards[Math.floor(Math.random() * standards.length)];
                    
                    grid[r][c] = {
                        type: chosenType,
                        gridX: c,
                        gridY: r,
                        x: targetX,
                        y: targetY,
                        targetY: targetY,
                        vy: 0,
                        scaleX: 1.0,
                        scaleY: 1.0,
                        bounceVel: 0,
                        state: 'resting',
                        isExploding: false,
                        explodeScale: 1.0
                    };
                }
            }
            updateUIState();
        }

        function initGrid() {
            for (let c = 0; c < gridCols; c++) {
                for (let r = 0; r < gridRows; r++) {
                    let spawnY = -100 - (gridRows - 1 - r) * (cellWidth + gap) - c * 48;
                    grid[r][c] = spawnSymbol(c, r, spawnY);
                }
            }
            gameState = 'falling';
        }

        function spawnSymbol(col, row, customY = null) {
            const standards = ['star', 'star', 'star', 'puffer', 'puffer', 'clam', 'clam', 'octopus', 'angler'];
            let chosenType = '';
            
            const specialRoll = Math.random();
            if (specialRoll < 0.04) {
                chosenType = 'blue_jelly'; 
            } else if (specialRoll < 0.08) {
                chosenType = 'pink_jelly'; 
            } else if (specialRoll < 0.11) {
                chosenType = 'gold_jelly'; 
            } else {
                chosenType = standards[Math.floor(Math.random() * standards.length)];
            }

            const targetX = gridStartX + col * (cellWidth + gap) + cellWidth / 2;
            const targetY = gridStartY + row * (cellWidth + gap) + cellWidth / 2;
            
            return {
                type: chosenType,
                gridX: col,
                gridY: row,
                x: targetX,
                y: customY !== null ? customY : -100,
                targetY: targetY,
                vy: 0,
                scaleX: 1.0,
                scaleY: 1.0,
                bounceVel: 0,
                state: 'falling',
                isExploding: false,
                explodeScale: 1.0
            };
        }

        function adjustBet(type) {
            if (gameState !== 'idle') return;
            if (type === 'half') {
                betAmount = Math.max(0.10, betAmount / 2);
            } else if (type === 'double') {
                betAmount = Math.min(100.00, betAmount * 2);
            }
            document.getElementById('bet-input').value = `$${betAmount.toFixed(2)}`;
            playSound('land', { pitch: 300 });
        }

        function toggleTurbo() {
            turboMode = !turboMode;
            const btn = document.getElementById('btn-turbo');
            if (turboMode) btn.classList.add('active');
            else btn.classList.remove('active');
            playSound('land', { pitch: 450 });
        }

        function toggleAuto() {
            autoSpin = !autoSpin;
            const btn = document.getElementById('btn-auto');
            if (autoSpin) btn.classList.add('active-gold');
            else btn.classList.remove('active-gold');
            playSound('land', { pitch: 550 });
            
            if (autoSpin && gameState === 'idle') {
                triggerSpin();
            }
        }

        function toggleMute() {
            isMuted = !isMuted;
            const btn = document.getElementById('btn-mute');
            if (isMuted) {
                btn.innerHTML = `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/><line x1="23" y1="9" x2="17" y2="15"/><line x1="17" y1="9" x2="23" y2="15"/></svg>`;
                btn.classList.remove('active');
                if (ambientGain) ambientGain.gain.setValueAtTime(0, audioCtx.currentTime);
            } else {
                btn.innerHTML = `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/><path d="M19.07 4.93a10 10 0 0 1 0 14.14M15.54 8.46a5 5 0 0 1 0 7.07"/></svg>`;
                btn.classList.add('active');
                if (audioCtx) {
                    audioCtx.resume();
                    if (ambientGain) ambientGain.gain.setValueAtTime(0.20, audioCtx.currentTime);
                } else {
                    initAudio();
                }
            }
        }

        function triggerBadgePulse(type) {
            const el = document.getElementById(type === 'size' ? 'stat-size-badge' : 'stat-mult-badge');
            if (!el) return;
            const cls = type === 'size' ? 'pulse-cyan' : 'pulse-magenta';
            el.classList.remove(cls);
            void el.offsetWidth; 
            el.classList.add(cls);
        }

        let lastUIState = {
            gameState: '',
            balance: -1,
            spinWin: -1,
            colossalSize: -1,
            colossalMult: -1,
            autoSpin: null
        };

        function updateUIState() {
            if (balance !== lastUIState.balance) {
                document.getElementById('balance-display').innerText = `$${balance.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2})}`;
                lastUIState.balance = balance;
            }
            if (spinWin !== lastUIState.spinWin) {
                document.getElementById('win-display').innerText = `$${spinWin.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2})}`;
                lastUIState.spinWin = spinWin;
            }
            if (colossalSize !== lastUIState.colossalSize) {
                document.getElementById('stat-size').innerText = `${colossalSize}x${colossalSize}`;
                lastUIState.colossalSize = colossalSize;
            }
            if (colossalMult !== lastUIState.colossalMult) {
                document.getElementById('stat-mult').innerText = `${colossalMult}x`;
                lastUIState.colossalMult = colossalMult;
            }
            
            if (gameState !== lastUIState.gameState || autoSpin !== lastUIState.autoSpin) {
                const spinBtn = document.getElementById('spin-button');
                if (gameState === 'idle') {
                    if (autoSpin) {
                        spinBtn.innerText = 'STOP AUTO';
                        spinBtn.disabled = false;
                        spinBtn.style.background = '#ff007f';
                        spinBtn.style.color = '#ffffff';
                        spinBtn.style.boxShadow = '0 0 15px rgba(255, 0, 127, 0.5)';
                    } else {
                        spinBtn.innerText = 'SPIN';
                        spinBtn.disabled = false;
                        spinBtn.style.background = '#00e701';
                        spinBtn.style.color = '#000000';
                        spinBtn.style.boxShadow = '0 0 15px rgba(0, 231, 1, 0.4)';
                    }
                } else {
                    spinBtn.innerText = autoSpin ? 'STOP AUTO' : 'STOP';
                    spinBtn.disabled = false;
                    spinBtn.style.background = '#ff007f';
                    spinBtn.style.color = '#ffffff';
                    spinBtn.style.boxShadow = '0 0 15px rgba(255, 0, 127, 0.5)';
                }
                lastUIState.gameState = gameState;
                lastUIState.autoSpin = autoSpin;
            }
        }

        function handleSpinClick() {
            if (gameState === 'idle') {
                if (autoSpin) {
                    toggleAuto();
                } else {
                    triggerSpin();
                }
            } else {
                if (autoSpin) {
                    autoSpin = false;
                    const btn = document.getElementById('btn-auto');
                    btn.classList.remove('active-gold');
                }
                triggerInstantStop();
            }
        }

        function triggerInstantStop() {
            playSound('land', { pitch: 600 });
            
            if (gameState === 'clearing_prev') {
                grid = Array(gridRows).fill(null).map(() => Array(gridCols).fill(null));
                colossalJelly = null;
                initGrid();
                landAllSymbols();
            } else if (gameState === 'falling' || gameState === 'landing_delay') {
                landAllSymbols();
            } else if (gameState === 'exploding') {
                timerDelay = 0;
            } else if (gameState === 'colossal_intro') {
                timerDelay = 0;
            } else if (gameState === 'colossal_falling') {
                if (colossalJelly) {
                    colossalJelly.y = colossalJelly.targetY;
                    colossalJelly.vy = 0;
                    colossalJelly.state = 'resting';
                    colossalJelly.bounceVel = -0.52;
                }
                gameState = 'colossal_impact';
                timerDelay = 0;
            }
            updateUIState();
        }

        function landAllSymbols() {
            for (let c = 0; c < gridCols; c++) {
                for (let r = 0; r < gridRows; r++) {
                    let sym = grid[r][c];
                    if (sym && sym.state === 'falling') {
                        sym.y = sym.targetY;
                        sym.vy = 0;
                        sym.state = 'resting';
                        sym.bounceVel = -0.36;
                    }
                }
            }
            anticipationActive = false;
            gameState = 'landing_delay';
            timerDelay = 0;
        }

        window.addEventListener('keydown', (e) => {
            if (e.code === 'Space') {
                e.preventDefault();
                handleSpinClick();
            }
        });


        function triggerSpin() {
            if (gameState !== 'idle') return;
            if (balance < betAmount) {
                balance = 1000.00;
                playSound('win_arpeggio', { multiplier: 3 });
                alertOverlay = { text: 'BALANCE REFILLED! +$1000', alpha: 1.0, timer: 120 };
            }
            
            balance -= betAmount;
            spinWin = 0.00;
            updateUIState();
            
            colossalSize = 2;
            colossalMult = 2;
            upgradesAcquiredThisSpin = false;
            colossalDroppedThisSpin = false;
            progressiveProgress = 0;
            currentProgress = 0;
            anticipationActive = false;

            playSound('spin');
            
            winCelebration.timer = 0;
            alertOverlay.timer = 0;
            coins = []; 
            flyingOrbs = [];
            impactRipples = [];

            // Sweep animation: old symbols fall off bottom quickly
            gameState = 'clearing_prev';
            for (let r = 0; r < gridRows; r++) {
                for (let c = 0; c < gridCols; c++) {
                    if (grid[r][c]) {
                        grid[r][c].state = 'clearing';
                        grid[r][c].vy = 4 + Math.random() * 6; // snap off the bottom
                    }
                }
            }
        }


        // --- DYNAMIC GRAPHICS CREATURE PROCEDURAL DRAWINGS ---
        function drawAnglerfish(ctx, x, y, size, phase) {
            ctx.save();
            ctx.translate(x, y);
            
            let bodyGrad = ctx.createRadialGradient(-size*0.1, -size*0.15, 2, 0, 0, size);
            bodyGrad.addColorStop(0, '#ffffff');
            bodyGrad.addColorStop(0.3, '#39ff14'); 
            bodyGrad.addColorStop(1, '#0c3300');
            
            ctx.fillStyle = bodyGrad;
            ctx.shadowBlur = 18 + Math.sin(phase * 1.5) * 5;
            ctx.shadowColor = '#39ff14';
            
            ctx.beginPath();
            ctx.ellipse(0, 0, size * 0.85, size * 0.7, 0, 0, Math.PI * 2);
            ctx.fill();
            
            ctx.fillStyle = 'rgba(255, 255, 255, 0.22)';
            ctx.shadowBlur = 0;
            ctx.beginPath();
            ctx.ellipse(0, -size * 0.2, size * 0.6, size * 0.25, -Math.PI / 10, 0, Math.PI, true);
            ctx.fill();
            
            let tailWobble = Math.sin(phase * 2.0) * 4;
            ctx.fillStyle = '#1c7700';
            ctx.beginPath();
            ctx.moveTo(-size * 0.8, 0);
            ctx.lineTo(-size * 1.2, -size * 0.35 + tailWobble);
            ctx.lineTo(-size * 1.05, 0);
            ctx.lineTo(-size * 1.2, size * 0.35 + tailWobble);
            ctx.closePath();
            ctx.fill();
            
            ctx.beginPath();
            ctx.ellipse(-size * 0.2, size * 0.1, size * 0.2, size * 0.15, Math.PI/4 + Math.sin(phase * 1.0)*0.15, 0, Math.PI*2);
            ctx.fill();

            ctx.fillStyle = '#220005';
            ctx.beginPath();
            ctx.moveTo(size * 0.2, size * 0.22);
            ctx.quadraticCurveTo(size * 0.5, size * 0.35, size * 0.75, size * 0.3);
            ctx.lineTo(size * 0.55, size * 0.05);
            ctx.closePath();
            ctx.fill();

            ctx.fillStyle = '#ffffff';
            ctx.beginPath();
            ctx.moveTo(size * 0.25, size * 0.2);
            ctx.lineTo(size * 0.28, size * 0.05);
            ctx.lineTo(size * 0.35, size * 0.2);
            ctx.moveTo(size * 0.40, size * 0.22);
            ctx.lineTo(size * 0.45, size * 0.08);
            ctx.lineTo(size * 0.52, size * 0.24);
            ctx.fill();
            
            ctx.fillStyle = '#ffd700';
            ctx.shadowBlur = 10;
            ctx.shadowColor = '#ffd700';
            for(let i=0; i<3; i++) {
                ctx.beginPath();
                ctx.arc(-size * 0.4 + i*size*0.2, size * 0.05 + Math.sin(phase * 1.2 + i)*1.5, 2.5, 0, Math.PI*2);
                ctx.fill();
            }

            ctx.fillStyle = '#ffaa00';
            ctx.shadowBlur = 10;
            ctx.shadowColor = '#ffaa00';
            ctx.beginPath();
            ctx.arc(size * 0.25, -size * 0.2, size * 0.16, 0, Math.PI * 2);
            ctx.fill();
            ctx.fillStyle = '#000000';
            ctx.shadowBlur = 0;
            ctx.beginPath();
            ctx.arc(size * 0.27, -size * 0.2, size * 0.06, 0, Math.PI * 2);
            ctx.fill();
            
            let rodWobble = Math.sin(phase * 1.5) * 6;
            ctx.strokeStyle = '#39ff14';
            ctx.lineWidth = 2.5;
            ctx.beginPath();
            ctx.moveTo(0, -size * 0.5);
            ctx.bezierCurveTo(size * 0.4, -size * 1.1 + rodWobble, size * 0.8, -size * 0.7 + rodWobble, size * 0.6, -size * 0.25 + rodWobble);
            ctx.stroke();
            
            ctx.fillStyle = '#ffffff';
            ctx.shadowBlur = 15 + Math.sin(phase * 4.0) * 8;
            ctx.shadowColor = '#ffd700';
            ctx.beginPath();
            ctx.arc(size * 0.6, -size * 0.25 + rodWobble, 6, 0, Math.PI*2);
            ctx.fill();
            
            ctx.restore();
        }

        function drawOctopus(ctx, x, y, size, phase) {
            ctx.save();
            ctx.translate(x, y);
            
            let baseColor = '#ff00aa';
            let secondaryColor = '#660033';
            ctx.shadowBlur = 16 + Math.sin(phase * 1.2) * 6;
            ctx.shadowColor = baseColor;
            
            ctx.globalAlpha = 0.8;
            const numTentacles = 6;
            for (let i = 0; i < numTentacles; i++) {
                let angle = (i / (numTentacles - 1)) * Math.PI * 0.8 - Math.PI * 0.4;
                let tx = Math.sin(angle) * size * 0.35;
                let ty = size * 0.12;
                
                let targetX = tx + Math.sin(angle) * size * 0.7;
                let targetY = ty + size * 0.75;
                let ctrlX = tx + Math.sin(angle + Math.sin(phase * 1.0 + i)*0.3) * size * 1.1;
                let ctrlY = ty + size * 0.35;
                
                ctx.lineWidth = 3.5;
                ctx.strokeStyle = baseColor;
                ctx.beginPath();
                ctx.moveTo(tx, ty);
                ctx.quadraticCurveTo(ctrlX, ctrlY, targetX + Math.sin(phase * 1.5 + i) * 6, targetY);
                ctx.stroke();
                
                ctx.fillStyle = '#ffffff';
                ctx.shadowBlur = 4;
                ctx.shadowColor = '#ffffff';
                ctx.beginPath();
                let cupX = (tx + ctrlX + targetX)/3 + Math.sin(phase*2.0 + i)*2 + 2;
                let cupY = (ty + ctrlY + targetY)/3 + 5;
                ctx.arc(cupX, cupY, 2, 0, Math.PI*2);
                ctx.arc(cupX - 5, cupY + 12, 1.8, 0, Math.PI*2);
                ctx.fill();
            }
            ctx.globalAlpha = 1.0;
            
            let bodyGrad = ctx.createRadialGradient(-size*0.08, -size*0.12, 1, 0, -size*0.05, size*0.65);
            bodyGrad.addColorStop(0, '#ff77dd');
            bodyGrad.addColorStop(0.5, baseColor);
            bodyGrad.addColorStop(1, secondaryColor);
            ctx.fillStyle = bodyGrad;
            ctx.beginPath();
            ctx.ellipse(0, -size * 0.1, size * 0.7, size * 0.6, 0, 0, Math.PI*2);
            ctx.fill();
            
            ctx.fillStyle = 'rgba(255, 255, 255, 0.28)';
            ctx.shadowBlur = 0;
            ctx.beginPath();
            ctx.ellipse(0, -size * 0.32, size * 0.45, size * 0.15, 0, 0, Math.PI * 2);
            ctx.fill();
            
            ctx.fillStyle = '#ffffff';
            ctx.beginPath();
            ctx.arc(-size * 0.2, -size * 0.05, size * 0.16, 0, Math.PI*2);
            ctx.arc(size * 0.2, -size * 0.05, size * 0.16, 0, Math.PI*2);
            ctx.fill();
            ctx.fillStyle = '#000000';
            ctx.beginPath();
            ctx.arc(-size * 0.18, -size * 0.04, size * 0.07, 0, Math.PI*2);
            ctx.arc(size * 0.18, -size * 0.04, size * 0.07, 0, Math.PI*2);
            ctx.fill();
            
            ctx.restore();
        }

        function drawClam(ctx, x, y, size, phase) {
            ctx.save();
            ctx.translate(x, y);
            
            let baseColor = '#9d00ff';
            let secondaryColor = '#3a005c';
            ctx.shadowBlur = 15 + Math.sin(phase * 1.2) * 5;
            ctx.shadowColor = baseColor;
            
            let openAmt = 0.16 + Math.sin(phase * 1.0) * 0.08;
            
            ctx.fillStyle = secondaryColor;
            ctx.strokeStyle = '#ffd700';
            ctx.lineWidth = 1.8;
            ctx.beginPath();
            ctx.arc(0, size * 0.15, size * 0.7, 0, Math.PI, false);
            ctx.closePath();
            ctx.fill();
            ctx.stroke();
            
            ctx.save();
            ctx.translate(0, size * 0.1);
            ctx.rotate(-openAmt);
            let shellGrad = ctx.createLinearGradient(0, -size * 0.7, 0, 0);
            shellGrad.addColorStop(0, '#e5b3ff');
            shellGrad.addColorStop(0.5, baseColor);
            shellGrad.addColorStop(1, secondaryColor);
            ctx.fillStyle = shellGrad;
            ctx.strokeStyle = '#ffd700'; 
            ctx.lineWidth = 1.8;
            
            ctx.beginPath();
            ctx.arc(0, -size * 0.08, size * 0.7, Math.PI, 0, false);
            ctx.lineTo(0, 0);
            ctx.closePath();
            ctx.fill();
            ctx.stroke();
            
            ctx.strokeStyle = 'rgba(255, 255, 255, 0.25)';
            ctx.lineWidth = 0.8;
            for (let i = -2; i <= 2; i++) {
                let angle = Math.PI / 2 + (i * 0.3);
                ctx.beginPath();
                ctx.moveTo(0, -size * 0.08);
                ctx.lineTo(Math.cos(angle) * size * 0.7, -size * 0.08 - Math.sin(angle) * size * 0.7);
                ctx.stroke();
            }
            ctx.restore();
            
            ctx.fillStyle = '#ffffff';
            ctx.shadowBlur = 18 + Math.sin(phase * 2.5) * 8;
            ctx.shadowColor = '#00f3ff';
            ctx.beginPath();
            ctx.arc(0, size * 0.1, 7.5, 0, Math.PI * 2);
            ctx.fill();
            
            let pearlGrad = ctx.createRadialGradient(0, size * 0.1, 0, 0, size * 0.1, 7.5);
            pearlGrad.addColorStop(0, '#ffffff');
            pearlGrad.addColorStop(0.5, '#e0ffff');
            pearlGrad.addColorStop(0.9, '#ff00aa');
            pearlGrad.addColorStop(1.0, 'transparent');
            ctx.fillStyle = pearlGrad;
            ctx.fill();
            
            ctx.restore();
        }

        function drawPufferfish(ctx, x, y, size, phase) {
            ctx.save();
            ctx.translate(x, y);
            
            let baseColor = '#00f3ff';
            let secondaryColor = '#00557c';
            ctx.shadowBlur = 14 + Math.sin(phase * 1.2) * 5;
            ctx.shadowColor = baseColor;
            
            let finWobble = Math.sin(phase * 2.0) * 4;
            ctx.fillStyle = '#0077aa';
            ctx.beginPath();
            ctx.moveTo(-size * 0.7, 0);
            ctx.lineTo(-size * 1.05, -size * 0.28 + finWobble);
            ctx.lineTo(-size * 1.05, size * 0.28 - finWobble);
            ctx.closePath();
            ctx.fill();
            
            let bodyPulse = 1.0 + Math.sin(phase * 1.2) * 0.04;
            let bodyR = size * 0.7 * bodyPulse;
            
            let bodyGrad = ctx.createRadialGradient(-size*0.2, -size*0.2, 2, 0, 0, bodyR * 1.1);
            bodyGrad.addColorStop(0, '#ffffff'); 
            bodyGrad.addColorStop(0.5, baseColor);
            bodyGrad.addColorStop(1, secondaryColor); 
            ctx.fillStyle = bodyGrad;
            ctx.beginPath();
            ctx.arc(0, 0, bodyR, 0, Math.PI*2);
            ctx.fill();
            
            ctx.fillStyle = '#00aae6';
            ctx.beginPath();
            ctx.ellipse(size * 0.65, 0, size*0.12, size*0.08, 0, 0, Math.PI*2);
            ctx.fill();
            ctx.fillStyle = '#ffffff';
            ctx.beginPath();
            ctx.ellipse(size * 0.67, 0, size*0.05, size*0.03, 0, 0, Math.PI*2);
            ctx.fill();

            ctx.strokeStyle = baseColor;
            ctx.lineWidth = 2.0;
            ctx.shadowBlur = 8;
            ctx.shadowColor = baseColor;
            const numSpikes = 12;
            for (let i = 0; i < numSpikes; i++) {
                let angle = (i / numSpikes) * Math.PI * 2;
                let sR = bodyR;
                let eR = bodyR + size * 0.18;
                ctx.beginPath();
                ctx.moveTo(Math.cos(angle) * sR, Math.sin(angle) * sR);
                ctx.lineTo(Math.cos(angle) * eR, Math.sin(angle) * eR);
                ctx.stroke();
            }
            ctx.shadowBlur = 0;
            
            ctx.fillStyle = '#ffffff';
            ctx.beginPath();
            ctx.arc(size * 0.28, -size * 0.12, 5.5, 0, Math.PI*2);
            ctx.fill();
            ctx.fillStyle = '#000000';
            ctx.beginPath();
            ctx.arc(size * 0.3, -size * 0.12, 2.5, 0, Math.PI*2);
            ctx.fill();
            
            ctx.restore();
        }

        function drawStarfish(ctx, x, y, size, phase) {
            ctx.save();
            ctx.translate(x, y);
            ctx.rotate(phase * 0.5);
            
            const points = 5;
            let bodyPulse = 1.0 + Math.sin(phase * 1.5) * 0.04;
            const outerR = size * 0.85 * bodyPulse;
            const innerR = size * 0.32 * bodyPulse;
            
            ctx.shadowBlur = 18 + Math.sin(phase * 1.5) * 6;
            ctx.shadowColor = '#ff4500';
            
            for (let i = 0; i < points; i++) {
                let angleCenter = (i / points) * Math.PI * 2 - Math.PI / 2;
                let angleLeft = ((i - 0.5) / points) * Math.PI * 2 - Math.PI / 2;
                let angleRight = ((i + 0.5) / points) * Math.PI * 2 - Math.PI / 2;
                
                ctx.fillStyle = '#ff6c2c'; 
                ctx.beginPath();
                ctx.moveTo(0, 0);
                ctx.lineTo(Math.cos(angleCenter) * outerR, Math.sin(angleCenter) * outerR);
                ctx.lineTo(Math.cos(angleLeft) * innerR, Math.sin(angleLeft) * innerR);
                ctx.closePath();
                ctx.fill();
                
                ctx.fillStyle = '#b32400'; 
                ctx.beginPath();
                ctx.moveTo(0, 0);
                ctx.lineTo(Math.cos(angleCenter) * outerR, Math.sin(angleCenter) * outerR);
                ctx.lineTo(Math.cos(angleRight) * innerR, Math.sin(angleRight) * innerR);
                ctx.closePath();
                ctx.fill();
            }
            
            ctx.fillStyle = '#ffd700';
            ctx.shadowBlur = 10;
            ctx.shadowColor = '#ffd700';
            ctx.beginPath();
            ctx.arc(0, 0, 4, 0, Math.PI*2);
            ctx.fill();
            
            ctx.restore();
        }

        // --- UPGRADE BONUS SPECIAL JELLYFISH ---
        function drawUpgradeJelly(ctx, x, y, size, phase, scaleX, scaleY, type) {
            let baseColor = (type === 'blue') ? '#00f3ff' : '#ff007f';
            let secondaryColor = (type === 'blue') ? '#0044aa' : '#aa0055';
            let tagText = (type === 'blue') ? 'SIZE UP' : 'MULT UP';
            
            ctx.save();
            ctx.translate(x, y);
            ctx.scale(scaleX, scaleY);
            
            ctx.shadowBlur = 20;
            ctx.shadowColor = baseColor;
            
            ctx.lineWidth = 2.0;
            ctx.strokeStyle = baseColor;
            ctx.globalAlpha = 0.6;
            
            const numTentacles = 4;
            for (let i = 0; i < numTentacles; i++) {
                let tx = -size * 0.4 + (i / (numTentacles - 1)) * size * 0.8;
                let ty = size * 0.15;
                ctx.beginPath();
                ctx.moveTo(tx, ty);
                let tLen = size * 0.95;
                ctx.lineTo(tx, ty + 4);
                for (let yOffset = 4; yOffset < tLen; yOffset += 4) {
                    let angle = phase + yOffset * 0.05 - i * 0.6;
                    let wx = tx + Math.sin(angle) * (4 + yOffset * 0.12);
                    ctx.lineTo(wx, ty + yOffset);
                }
                ctx.stroke();
            }

            ctx.globalAlpha = 1.0;
            let capGrad = ctx.createRadialGradient(0, -size * 0.1, 2, 0, 0, size * 0.8);
            capGrad.addColorStop(0, '#ffffff');
            capGrad.addColorStop(0.3, baseColor);
            capGrad.addColorStop(1, secondaryColor);
            
            ctx.fillStyle = capGrad;
            ctx.beginPath();
            ctx.arc(0, -size * 0.05, size * 0.75, Math.PI, 0, false);
            ctx.bezierCurveTo(size * 0.4, size * 0.2, size * 0.2, size * 0.1, 0, size * 0.1);
            ctx.bezierCurveTo(-size * 0.2, size * 0.1, -size * 0.4, size * 0.2, -size * 0.75, -size * 0.05);
            ctx.closePath();
            ctx.fill();

            ctx.restore();
            
            // Draw tag
            ctx.save();
            ctx.translate(x, y - size * 0.6);
            ctx.fillStyle = 'rgba(15, 33, 46, 0.9)';
            ctx.strokeStyle = baseColor;
            ctx.lineWidth = 1;
            ctx.shadowBlur = 5;
            ctx.shadowColor = baseColor;
            
            ctx.beginPath();
            ctx.roundRect(-24, -7, 48, 14, 4);
            ctx.fill();
            ctx.stroke();
            
            ctx.fillStyle = '#ffffff';
            ctx.shadowBlur = 0;
            ctx.font = '800 7.5px "Outfit", sans-serif';
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            ctx.fillText(tagText, 0, 0);
            ctx.restore();
        }

        // Gold Scatter Jelly
        function drawGoldScatterJelly(ctx, x, y, size, phase, scaleX, scaleY) {
            ctx.save();
            ctx.translate(x, y);
            ctx.scale(scaleX, scaleY);
            
            ctx.shadowBlur = 22;
            ctx.shadowColor = '#ffd700';
            
            ctx.lineWidth = 2.0;
            ctx.strokeStyle = '#ffd700';
            ctx.globalAlpha = 0.65;
            for (let i = 0; i < 4; i++) {
                let tx = -size * 0.4 + (i / 3) * size * 0.8;
                let ty = size * 0.15;
                ctx.beginPath();
                ctx.moveTo(tx, ty);
                let tLen = size * 0.95;
                ctx.lineTo(tx, ty + 4);
                for (let yOffset = 4; yOffset < tLen; yOffset += 4) {
                    let angle = phase + yOffset * 0.05 - i * 0.6;
                    ctx.lineTo(tx + Math.sin(angle) * (4 + yOffset * 0.12), ty + yOffset);
                }
                ctx.stroke();
            }

            ctx.globalAlpha = 1.0;
            let capGrad = ctx.createRadialGradient(0, -size * 0.1, 2, 0, 0, size * 0.8);
            capGrad.addColorStop(0, '#ffffff');
            capGrad.addColorStop(0.3, '#ffd700');
            capGrad.addColorStop(1, '#664400');
            ctx.fillStyle = capGrad;
            ctx.beginPath();
            ctx.arc(0, -size * 0.05, size * 0.75, Math.PI, 0, false);
            ctx.bezierCurveTo(size * 0.4, size * 0.2, size * 0.2, size * 0.1, 0, size * 0.1);
            ctx.bezierCurveTo(-size * 0.2, size * 0.1, -size * 0.4, size * 0.2, -size * 0.75, -size * 0.05);
            ctx.closePath();
            ctx.fill();
            ctx.restore();
            
            ctx.save();
            ctx.translate(x, y - size * 0.6);
            ctx.fillStyle = 'rgba(15, 33, 46, 0.9)';
            ctx.strokeStyle = '#ffd700';
            ctx.lineWidth = 1;
            ctx.shadowBlur = 5;
            ctx.shadowColor = '#ffd700';
            ctx.beginPath();
            ctx.roundRect(-24, -7, 48, 14, 4);
            ctx.fill();
            ctx.stroke();
            ctx.fillStyle = '#ffd700';
            ctx.shadowBlur = 0;
            ctx.font = '800 7.5px "Outfit", sans-serif';
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            ctx.fillText('SCATTER', 0, 0);
            ctx.restore();
        }

        // Colossal Golden Jellyfish (The giant drop)
        function drawColossalJellyfish(ctx, x, y, size, phase, scaleX, scaleY, multiplier) {
            ctx.save();
            ctx.translate(x, y);
            ctx.scale(scaleX, scaleY);
            
            let baseColor = '#ffd700'; 
            ctx.shadowBlur = 35;
            ctx.shadowColor = baseColor;
            
            ctx.lineWidth = 4.5;
            ctx.strokeStyle = baseColor;
            ctx.globalAlpha = 0.65;
            const numTentacles = 8;
            for (let i = 0; i < numTentacles; i++) {
                let tx = -size * 0.5 + (i / (numTentacles - 1)) * size * 1.0;
                let ty = size * 0.12;
                ctx.beginPath();
                ctx.moveTo(tx, ty);
                let waveFreq = 0.025;
                let waveAmp = 10;
                let tentacleLen = size * 1.2;
                ctx.lineTo(tx, ty + 8);
                for (let yOffset = 8; yOffset < tentacleLen; yOffset += 6) {
                    let angle = phase + yOffset * waveFreq - i * 0.5;
                    let wx = tx + Math.sin(angle) * (waveAmp + yOffset * 0.12);
                    ctx.lineTo(wx, ty + yOffset);
                }
                ctx.stroke();
            }

            ctx.globalAlpha = 1.0;
            let capGrad = ctx.createRadialGradient(0, -size * 0.12, 5, 0, 0, size * 0.9);
            capGrad.addColorStop(0, '#ffffff');
            capGrad.addColorStop(0.3, baseColor);
            capGrad.addColorStop(1, '#552200');
            ctx.fillStyle = capGrad;
            ctx.beginPath();
            ctx.moveTo(-size * 0.85, -size * 0.08);
            ctx.bezierCurveTo(-size * 0.85, -size * 0.65, -size * 0.5, -size * 0.85, -size * 0.35, -size * 0.85);
            ctx.lineTo(-size * 0.22, -size * 0.58);
            ctx.lineTo(0, -size * 0.95); 
            ctx.lineTo(size * 0.22, -size * 0.58);
            ctx.lineTo(size * 0.35, -size * 0.85);
            ctx.bezierCurveTo(size * 0.5, -size * 0.85, size * 0.9, -size * 0.65, size * 0.85, -size * 0.08);
            ctx.bezierCurveTo(size * 0.5, size * 0.22, size * 0.25, size * 0.1, 0, size * 0.1);
            ctx.bezierCurveTo(-size * 0.25, size * 0.1, -size * 0.5, size * 0.22, -size * 0.85, -size * 0.08);
            ctx.closePath();
            ctx.fill();
            
            ctx.beginPath();
            ctx.arc(0, -size * 0.2, size * 0.32, 0, Math.PI * 2);
            let coreGrad = ctx.createRadialGradient(0, -size * 0.2, 0, 0, -size * 0.2, size * 0.32);
            coreGrad.addColorStop(0, '#ffffff');
            coreGrad.addColorStop(0.4, '#ffd700');
            coreGrad.addColorStop(1, 'transparent');
            ctx.fillStyle = coreGrad;
            ctx.fill();
            
            ctx.fillStyle = '#ff1100';
            ctx.shadowBlur = 12;
            ctx.shadowColor = '#ff1100';
            ctx.beginPath();
            ctx.arc(-size * 0.35, -size * 0.85, 4.5, 0, Math.PI * 2);
            ctx.arc(0, -size * 0.95, 5.5, 0, Math.PI * 2);
            ctx.arc(size * 0.35, -size * 0.85, 4.5, 0, Math.PI * 2);
            ctx.fill();
            ctx.restore();
            
            // Multiplier Board
            ctx.save();
            ctx.translate(x, y - 5);
            ctx.fillStyle = 'rgba(15, 33, 46, 0.93)';
            ctx.strokeStyle = '#ffd700';
            ctx.lineWidth = 2.5;
            ctx.shadowBlur = 15;
            ctx.shadowColor = '#ffd700';
            let w = 82;
            let h = 32;
            ctx.beginPath();
            ctx.roundRect(-w / 2, -h / 2, w, h, 6);
            ctx.fill();
            ctx.stroke();
            
            ctx.fillStyle = '#ffffff';
            ctx.shadowBlur = 0;
            ctx.font = '800 11px "Outfit", sans-serif';
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            ctx.fillText('COLOSSAL', 0, -22);
            ctx.fillStyle = '#ffd700';
            ctx.font = '800 19px "Outfit", sans-serif';
            ctx.fillText(`x${multiplier}`, 0, 1);
            ctx.restore();
        }

        // --- PARTICLE EX EXPLOSIONS ---
        function spawnClusterExplosion(x, y, color) {
            const count = 20 + Math.floor(Math.random() * 6);
            for (let i = 0; i < count; i++) {
                let angle = Math.random() * Math.PI * 2;
                let vel = 1.5 + Math.random() * 2.0; // Halved velocity for gentle rise
                particles.push({
                    x: x,
                    y: y,
                    vx: Math.cos(angle) * vel,
                    vy: Math.sin(angle) * vel,
                    r: 1.5 + Math.random() * 3.5,
                    color: color,
                    type: Math.random() < 0.5 ? 'droplet' : 'bubble',
                    life: 0,
                    maxLife: 35 + Math.floor(Math.random() * 15)
                });
            }
        }

        // Gold coin shower on big wins
        function spawnCoinShower(winAmt) {
            let count = Math.min(40 + Math.floor(winAmt * 2.5), 100);
            for (let i = 0; i < count; i++) {
                coins.push({
                    x: Math.random() * canvas.width,
                    y: -50 - Math.random() * 200,
                    vx: -1.5 + Math.random() * 3,
                    vy: 4 + Math.random() * 6,
                    r: 5 + Math.random() * 3,
                    angle: Math.random() * Math.PI * 2,
                    rotationSpeed: 0.05 + Math.random() * 0.15,
                    life: 0,
                    maxLife: 150
                });
            }
        }

        function spawnFlyingOrb(startX, startY, type, val) {
            let targetX = 0, targetY = 0;
            let color = '';
            
            if (type === 'size') {
                targetX = 440; // Target Size Badge
                targetY = -15;
                color = '#00f3ff';
            } else if (type === 'mult') {
                targetX = 520; // Target Mult Badge
                targetY = -15;
                color = '#ff007f';
            } else {
                targetX = 300; // Target progressive charge bar center
                targetY = 38;
                color = '#ffd700';
            }

            // Curve control point (arcs upwards)
            let ctrlX = (startX + targetX) / 2 + (Math.random() - 0.5) * 80;
            let ctrlY = Math.min(startY, targetY) - 130;

            flyingOrbs.push({
                startX: startX,
                startY: startY,
                targetX: targetX,
                targetY: targetY,
                ctrlX: ctrlX,
                ctrlY: ctrlY,
                progress: 0.0,
                speed: 0.02 + Math.random() * 0.008, 
                color: color,
                type: type,
                val: val
            });
            playSound('spin', { pitch: 550 });
        }

        function updateAndDrawParticles() {
            // update flying orbs
            for (let i = flyingOrbs.length - 1; i >= 0; i--) {
                let o = flyingOrbs[i];
                o.progress += o.speed;
                
                let t = o.progress;
                if (t >= 1.0) {
                    if (o.type === 'size') {
                        colossalSize = Math.min(6, colossalSize + o.val);
                        triggerBadgePulse('size');
                    } else if (o.type === 'mult') {
                        colossalMult = Math.min(100, colossalMult + o.val);
                        triggerBadgePulse('mult');
                        playSound('upgrade');
                    } else if (o.type === 'charge') {
                        progressiveProgress = Math.min(100, progressiveProgress + o.val);
                        playSound('upgrade');
                    }
                    updateUIState();
                    
                    for (let p = 0; p < 15; p++) {
                        let angle = Math.random() * Math.PI*2;
                        let vel = 1 + Math.random()*3;
                        particles.push({
                            x: o.targetX,
                            y: o.targetY,
                            vx: Math.cos(angle)*vel,
                            vy: Math.sin(angle)*vel,
                            r: 1.5 + Math.random()*2,
                            color: o.color,
                            type: 'droplet',
                            life: 0,
                            maxLife: 20
                        });
                    }
                    
                    flyingOrbs.splice(i, 1);
                    continue;
                }

                let ox = (1-t)*(1-t)*o.startX + 2*(1-t)*t*o.ctrlX + t*t*o.targetX;
                let oy = (1-t)*(1-t)*o.startY + 2*(1-t)*t*o.ctrlY + t*t*o.targetY;
                
                particles.push({
                    x: ox,
                    y: oy,
                    vx: (Math.random()-0.5)*1.5,
                    vy: (Math.random()-0.5)*1.5,
                    r: 2 + Math.random()*2,
                    color: o.color,
                    type: 'droplet',
                    life: 0,
                    maxLife: 20
                });

                ctx.save();
                ctx.shadowBlur = 18;
                ctx.shadowColor = o.color;
                ctx.fillStyle = '#ffffff';
                ctx.beginPath();
                ctx.arc(ox, oy, 7, 0, Math.PI*2);
                ctx.fill();
                ctx.restore();
            }

            // Normal particles
            for (let i = particles.length - 1; i >= 0; i--) {
                let p = particles[i];
                p.life++;
                p.vx *= 0.94; // Soft resistance slow down
                p.vy *= 0.94;
                
                if (p.type === 'bubble') p.vy -= 0.06; // Slow drift up
                else p.vy += 0.03; 
                
                p.x += p.vx;
                p.y += p.vy;
                
                let opacity = 1.0 - (p.life / p.maxLife);
                if (opacity <= 0 || p.life >= p.maxLife) {
                    particles.splice(i, 1);
                    continue;
                }
                
                ctx.save();
                ctx.globalAlpha = opacity;
                ctx.shadowBlur = 10;
                ctx.shadowColor = p.color;
                
                if (p.type === 'bubble') {
                    ctx.strokeStyle = '#ffffff';
                    ctx.lineWidth = 1;
                    ctx.beginPath();
                    ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
                    ctx.stroke();
                } else {
                    ctx.fillStyle = p.color;
                    ctx.beginPath();
                    ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
                    ctx.fill();
                }
                ctx.restore();
            }

            // Coin particles update
            for (let i = coins.length - 1; i >= 0; i--) {
                let c = coins[i];
                c.y += c.vy;
                c.x += c.vx;
                c.angle += c.rotationSpeed;
                c.life++;
                
                if (c.y > canvas.height + 20 || c.life > c.maxLife) {
                    coins.splice(i, 1);
                    continue;
                }

                if (Math.random() < 0.015) playSound('coin');

                ctx.save();
                ctx.translate(c.x, c.y);
                ctx.rotate(c.angle);
                ctx.shadowBlur = 8;
                ctx.shadowColor = '#ffd700';
                
                let coinGrad = ctx.createRadialGradient(0, 0, 1, 0, 0, c.r);
                coinGrad.addColorStop(0, '#ffffff');
                coinGrad.addColorStop(0.3, '#ffd700');
                coinGrad.addColorStop(1, '#ff8800');
                
                ctx.fillStyle = coinGrad;
                ctx.beginPath();
                ctx.ellipse(0, 0, c.r, c.r * Math.abs(Math.sin(c.angle)), 0, 0, Math.PI * 2);
                ctx.fill();
                ctx.restore();
            }

            // Impact ripples updates
            for (let i = impactRipples.length - 1; i >= 0; i--) {
                let r = impactRipples[i];
                r.r += 1.6;
                r.alpha -= 0.05;
                if (r.alpha <= 0 || r.r >= r.maxR) {
                    impactRipples.splice(i, 1);
                    continue;
                }
                ctx.save();
                ctx.globalAlpha = r.alpha;
                ctx.strokeStyle = r.color;
                ctx.lineWidth = 2.0;
                ctx.beginPath();
                ctx.ellipse(r.x, r.y, r.r, r.r * 0.25, 0, 0, Math.PI * 2);
                ctx.stroke();
                ctx.restore();
            }
        }

        // --- SHOCKWAVE SYSTEM ---
        function updateAndDrawShockwaves() {
            for (let i = shockwaves.length - 1; i >= 0; i--) {
                let s = shockwaves[i];
                s.radius += s.speed;
                s.alpha = 1 - (s.radius / s.maxRadius);
                
                if (s.radius >= s.maxRadius || s.alpha <= 0) {
                    shockwaves.splice(i, 1);
                    continue;
                }
                
                ctx.save();
                ctx.strokeStyle = `rgba(255, 215, 0, ${s.alpha})`;
                ctx.lineWidth = s.width * s.alpha;
                ctx.shadowBlur = 30;
                ctx.shadowColor = '#ffd700';
                ctx.beginPath();
                ctx.arc(s.x, s.y, s.radius, 0, Math.PI * 2);
                ctx.stroke();
                ctx.restore();
            }
        }

        // --- FLOATING TEXT ---
        function updateAndDrawFloatingTexts() {
            for (let i = floatingTexts.length - 1; i >= 0; i--) {
                let ft = floatingTexts[i];
                ft.y -= ft.vy;
                ft.life++;
                let opacity = 1.0 - (ft.life / ft.maxLife);
                if (opacity <= 0) {
                    floatingTexts.splice(i, 1);
                    continue;
                }
                ctx.save();
                ctx.globalAlpha = opacity;
                ctx.textAlign = 'center';
                ctx.font = `800 ${ft.size}px "Outfit", sans-serif`;
                ctx.shadowBlur = 12;
                ctx.shadowColor = ft.color;
                ctx.fillStyle = ft.color;
                ctx.fillText(ft.text, ft.x, ft.y);
                ctx.restore();
            }
        }


        // --- FLOOD FILL CLUSTER SOLVER ---
        function getCluster(startRow, startCol, matchType) {
            const cluster = [];
            const queue = [{ r: startRow, c: startCol }];
            const visited = Array(gridRows).fill(null).map(() => Array(gridCols).fill(false));
            visited[startRow][startCol] = true;

            while (queue.length > 0) {
                const current = queue.shift();
                cluster.push(current);
                const directions = [{r:-1,c:0},{r:1,c:0},{r:0,c:-1},{r:0,c:1}];
                for (let dir of directions) {
                    const nr = current.r + dir.r;
                    const nc = current.c + dir.c;
                    if (nr >= 0 && nr < gridRows && nc >= 0 && nc < gridCols) {
                        if (!visited[nr][nc] && grid[nr][nc] && !grid[nr][nc].isExploding) {
                            if (grid[nr][nc].type === matchType && !grid[nr][nc].isColossal) {
                                visited[nr][nc] = true;
                                queue.push({ r: nr, c: nc });
                            }
                        }
                    }
                }
            }
            return cluster;
        }

        function resolveGridClusters() {
            const visited = Array(gridRows).fill(null).map(() => Array(gridCols).fill(false));
            const allClusters = [];

            // Standard cluster matches
            for (let r = 0; r < gridRows; r++) {
                for (let c = 0; c < gridCols; c++) {
                    const sym = grid[r][c];
                    if (sym && !sym.isExploding && !visited[r][c] && !sym.isColossal && 
                        sym.type !== 'blue_jelly' && sym.type !== 'pink_jelly' && sym.type !== 'gold_jelly') {
                        
                        const cluster = getCluster(r, c, sym.type);
                        for (let cell of cluster) visited[cell.r][cell.c] = true;
                        if (cluster.length >= 5) {
                            allClusters.push({
                                type: sym.type,
                                cells: cluster
                            });
                        }
                    }
                }
            }

            // Colossal matches
            let colossalFound = false;
            let colossalObj = null;
            for (let r = 0; r < gridRows; r++) {
                for (let c = 0; c < gridCols; c++) {
                    if (grid[r][c] && grid[r][c].isColossal) {
                        colossalFound = true;
                        colossalObj = grid[r][c];
                        break;
                    }
                }
                if (colossalFound) break;
            }

            if (colossalFound && colossalObj && colossalObj.state === 'resting') {
                const colossalCells = [];
                const visitedMatch = Array(gridRows).fill(null).map(() => Array(gridCols).fill(false));
                
                const S = colossalObj.size;
                const sc = colossalObj.gridX;
                const sr = colossalObj.gridY;
                
                for (let r = sr; r < sr + S; r++) {
                    for (let c = sc; c < sc + S; c++) colossalCells.push({ r: r, c: c });
                }

                const matchType = colossalSymbolToConvert;
                const queue = [];
                
                for (let r = sr; r < sr + S; r++) {
                    if (sc - 1 >= 0 && grid[r][sc - 1] && grid[r][sc - 1].type === matchType && !grid[r][sc - 1].isExploding) {
                        if (!visitedMatch[r][sc - 1]) {
                            visitedMatch[r][sc - 1] = true;
                            queue.push({ r: r, c: sc - 1 });
                        }
                    }
                    if (sc + S < gridCols && grid[r][sc + S] && grid[r][sc + S].type === matchType && !grid[r][sc + S].isExploding) {
                        if (!visitedMatch[r][sc + S]) {
                            visitedMatch[r][sc + S] = true;
                            queue.push({ r: r, c: sc + S });
                        }
                    }
                }
                for (let c = sc; c < sc + S; c++) {
                    if (sr - 1 >= 0 && grid[sr - 1][c] && grid[sr - 1][c].type === matchType && !grid[sr - 1][c].isExploding) {
                        if (!visitedMatch[sr - 1][c]) {
                            visitedMatch[sr - 1][c] = true;
                            queue.push({ r: sr - 1, c: c });
                        }
                    }
                    if (sr + S < gridRows && grid[sr + S][c] && grid[sr + S][c].type === matchType && !grid[sr + S][c].isExploding) {
                        if (!visitedMatch[sr + S][c]) {
                            visitedMatch[sr + S][c] = true;
                            queue.push({ r: sr + S, c: c });
                        }
                    }
                }

                while (queue.length > 0) {
                    const current = queue.shift();
                    colossalCells.push(current);
                    const dirs = [{r:-1,c:0},{r:1,c:0},{r:0,c:-1},{r:0,c:1}];
                    for (let d of dirs) {
                        const nr = current.r + d.r;
                        const nc = current.c + d.c;
                        if (nr >= 0 && nr < gridRows && nc >= 0 && nc < gridCols) {
                            const inCol = (nr >= sr && nr < sr + S && nc >= sc && nc < sc + S);
                            if (!inCol && !visitedMatch[nr][nc] && grid[nr][nc] && grid[nr][nc].type === matchType && !grid[nr][nc].isExploding) {
                                visitedMatch[nr][nc] = true;
                                queue.push({ r: nr, c: nc });
                            }
                        }
                    }
                }

                allClusters.push({
                    type: 'colossal',
                    cells: colossalCells,
                    colossalObj: colossalObj
                });
            }

            return allClusters;
        }

        // --- UPDATE ENGINE TICK ---
        function update(time) {
            let dt = time - lastTime;
            if (dt > 100) dt = 16.67; 
            lastTime = time;
            
            let dtFactor = dt / 16.67;

            if (shakeIntensity > 0.05) shakeIntensity *= 0.88;
            else shakeIntensity = 0;

            if (currentProgress < progressiveProgress) {
                currentProgress += (progressiveProgress - currentProgress) * 0.1;
            } else if (currentProgress > progressiveProgress) {
                currentProgress += (progressiveProgress - currentProgress) * 0.1;
            }

            for (let b of bubbles) {
                b.y += b.vy;
                b.vx = Math.sin(time * b.wobbleSpeed) * (b.wobbleAmt * 0.08);
                b.x += b.vx;
                if (b.y < -10) {
                    b.y = canvas.height + 20;
                    b.x = Math.random() * canvas.width;
                }
            }

            // Plankton drifting background simulation
            for (let p of bgPlankton) {
                p.x += Math.sin(time * 0.001 + p.angle) * p.speed;
                p.y -= p.speed * 0.6;
                p.opacity = (0.2 + Math.abs(Math.sin(time * p.pulseSpeed)) * 0.6) * 0.5;
                if (p.y < -10) {
                    p.y = canvas.height + 10;
                    p.x = Math.random() * canvas.width;
                }
            }

            for (let bg of bgCreatures) {
                bg.x += bg.speed * bg.scaleX;
                if (bg.scaleX === 1 && bg.x > canvas.width + bg.width + 50) {
                    bg.x = -bg.width - 50;
                    bg.y = 150 + Math.random() * 300;
                } else if (bg.scaleX === -1 && bg.x < -bg.width - 50) {
                    bg.x = canvas.width + bg.width + 50;
                    bg.y = 150 + Math.random() * 300;
                }
            }

            switch (gameState) {
                case 'clearing_prev': {
                    let clearingActive = false;
                    for (let r = 0; r < gridRows; r++) {
                        for (let c = 0; c < gridCols; c++) {
                            let sym = grid[r][c];
                            if (sym) {
                                sym.y += sym.vy * dtFactor;
                                sym.vy += 0.95 * dtFactor;
                                if (sym.y < canvas.height + 100) clearingActive = true;
                            }
                        }
                    }
                    if (!clearingActive) {
                        grid = Array(gridRows).fill(null).map(() => Array(gridCols).fill(null));
                        colossalJelly = null;
                        initGrid();
                    }
                    break;
                }

                case 'falling': {
                    let allLanded = true;
                    anticipationActive = false;

                    let scattersLanded = 0;
                    for (let c = 0; c < gridCols; c++) {
                        for (let r = 0; r < gridRows; r++) {
                            let sym = grid[r][c];
                            if (sym && sym.state === 'resting' && sym.type === 'gold_jelly') {
                                scattersLanded++;
                            }
                        }
                    }

                    for (let c = 0; c < gridCols; c++) {
                        let colAnticipation = (scattersLanded >= 2);
                        if (colAnticipation) {
                            let prevColsLanded = true;
                            for (let pc = 0; pc < c; pc++) {
                                for (let pr = 0; pr < gridRows; pr++) {
                                    if (grid[pr][pc] && grid[pr][pc].state === 'falling') {
                                        prevColsLanded = false;
                                        break;
                                    }
                                }
                            }
                            if (prevColsLanded) {
                                anticipationActive = true;
                            }
                        }

                        const grav = turboMode ? 1.5 : (anticipationActive ? 0.22 : 0.55);
                        const drag = turboMode ? 0.90 : (anticipationActive ? 0.94 : 0.95);
                        
                        for (let r = 0; r < gridRows; r++) {
                            let sym = grid[r][c];
                            if (sym && sym.state === 'falling') {
                                allLanded = false;
                                sym.vy = sym.vy * Math.pow(drag, dtFactor) + grav * dtFactor;
                                sym.y += sym.vy * dtFactor;
                                
                                // Spawn a trail particle behind the falling creature!
                                if (Math.random() < 0.12 * dtFactor) {
                                    particles.push({
                                        x: sym.x + (Math.random() - 0.5) * 20,
                                        y: sym.y + 15,
                                        vx: (Math.random() - 0.5) * 0.4,
                                        vy: sym.vy * 0.2,
                                        r: 1 + Math.random() * 2,
                                        color: 'rgba(0, 243, 255, 0.4)',
                                        type: 'droplet',
                                        life: 0,
                                        maxLife: 30
                                    });
                                }
                                
                                if (sym.y >= sym.targetY) {
                                    sym.y = sym.targetY;
                                    sym.vy = 0;
                                    sym.state = 'resting';
                                    sym.bounceVel = -0.36; // snappy rubbery bounce 
                                    
                                    let colColors = { 'star':'#ff4500', 'puffer':'#00f3ff', 'clam':'#9d00ff', 'octopus':'#ff00aa', 'angler':'#39ff14', 'blue_jelly':'#00f3ff', 'pink_jelly':'#ff007f', 'gold_jelly':'#ffd700'};
                                    impactRipples.push({
                                        x: sym.x,
                                        y: sym.y + 15,
                                        r: 3,
                                        maxR: 26,
                                        alpha: 0.8,
                                        color: colColors[sym.type] || '#ffffff'
                                    });

                                    playSound('land', { pitch: 80 + c * 10 });
                                }
                            }
                        }
                    }

                    for (let r = 0; r < gridRows; r++) {
                        for (let c = 0; c < gridCols; c++) {
                            let sym = grid[r][c];
                            if (sym && sym.state === 'resting') {
                                updateSoftBodyWobble(sym, dtFactor);
                            }
                        }
                    }

                    if (allLanded) {
                        gameState = 'landing_delay';
                        timerDelay = turboMode ? 40 : 150; 
                    }
                    break;
                }

                case 'landing_delay': {
                    timerDelay -= dt;
                    for (let r = 0; r < gridRows; r++) {
                        for (let c = 0; c < gridCols; c++) {
                            if (grid[r][c]) updateSoftBodyWobble(grid[r][c], dtFactor);
                        }
                    }
                    if (timerDelay <= 0) {
                        gameState = 'check_wins';
                    }
                    break;
                }

                case 'check_wins': {
                    let upgradesFound = false;
                    if (!colossalDroppedThisSpin) {
                        for (let r = 0; r < gridRows; r++) {
                            for (let c = 0; c < gridCols; c++) {
                                let sym = grid[r][c];
                                if (sym && !sym.isExploding) {
                                    if (sym.type === 'blue_jelly') {
                                        upgradesAcquiredThisSpin = true;
                                        upgradesFound = true;
                                        sym.isExploding = true;
                                        spawnFlyingOrb(sym.x, sym.y, 'size', 1);
                                    }
                                    else if (sym.type === 'pink_jelly') {
                                        upgradesAcquiredThisSpin = true;
                                        upgradesFound = true;
                                        sym.isExploding = true;
                                        spawnFlyingOrb(sym.x, sym.y, 'mult', 2);
                                    }
                                    else if (sym.type === 'gold_jelly') {
                                        upgradesFound = true;
                                        sym.isExploding = true;
                                        spawnFlyingOrb(sym.x, sym.y, 'charge', 15);
                                    }
                                }
                            }
                        }
                    }

                    if (upgradesFound) {
                        timerDelay = turboMode ? 200 : 700; 
                        gameState = 'exploding';
                        break;
                    }

                    const matches = resolveGridClusters();
                    if (matches.length > 0) {
                        let totalSpinWin = 0;
                        activeClusters = matches; 
                        
                        for (let cl of matches) {
                            let baseType = cl.type;
                            let cells = cl.cells;
                            let count = cells.length;
                            
                            let sumX = 0;
                            let sumY = 0;

                            for (let cell of cells) {
                                let sym = grid[cell.r][cell.c];
                                sumX += sym.x;
                                sumY += sym.y;
                                sym.isExploding = true;
                                sym.explodeScale = 1.0;
                            }

                            let centerX = sumX / count;
                            let centerY = sumY / count;
                            let clusterWin = 0;
                            
                            let colorMap = {
                                'star': '#ff4500',
                                'puffer': '#00f3ff',
                                'clam': '#9d00ff',
                                'octopus': '#ff00aa',
                                'angler': '#39ff14',
                                'colossal': '#ffd700'
                            };

                            if (baseType === 'colossal') {
                                let payRate = payouts[colossalSymbolToConvert] || 0.1;
                                clusterWin = count * payRate * colossalMult * betAmount;
                                colossalJelly.isExploding = true;
                                colossalJelly.explodeScale = 1.0;
                            } else {
                                let basePay = payouts[baseType] * betAmount;
                                clusterWin = count * basePay;
                            }

                            totalSpinWin += clusterWin;
                        }

                        spinWin += totalSpinWin;
                        balance += totalSpinWin;
                        updateUIState();
                        
                        let mt = totalSpinWin / betAmount;
                        if (mt >= 50.0) {
                            winCelebration = { text: 'COLOSSAL WIN!', winAmt: totalSpinWin, timer: 120, scale: 0 };
                            playSound('win_arpeggio', { multiplier: 7 });
                            spawnCoinShower(totalSpinWin);
                        } else if (mt >= 20.0) {
                            winCelebration = { text: 'MEGA WIN!', winAmt: totalSpinWin, timer: 100, scale: 0 };
                            playSound('win_arpeggio', { multiplier: 5 });
                            spawnCoinShower(totalSpinWin);
                        } else if (mt >= 5.0) {
                            winCelebration = { text: 'BIG WIN!', winAmt: totalSpinWin, timer: 80, scale: 0 };
                            playSound('win_arpeggio', { multiplier: 2.5 });
                            spawnCoinShower(totalSpinWin);
                        } else {
                            playSound('win_arpeggio', { multiplier: 1 });
                        }

                        // Soft screenshake rumble
                        shakeIntensity = Math.min(10, shakeIntensity + totalSpinWin * 0.8);
                        timerDelay = turboMode ? 250 : 700; // Longer pause to let laser connections show!
                        gameState = 'exploding';
                    } else {
                        if (!colossalDroppedThisSpin && (upgradesAcquiredThisSpin || progressiveProgress >= 100)) {
                            colossalDroppedThisSpin = true;
                            upgradesAcquiredThisSpin = false;
                            progressiveProgress = 0; 
                            gameState = 'colossal_intro';
                            timerDelay = turboMode ? 300 : 800;
                        } else {
                            gameState = 'idle';
                            updateUIState();
                            
                            if (autoSpin) {
                                setTimeout(() => {
                                    if (autoSpin && gameState === 'idle') {
                                        triggerSpin();
                                    }
                                }, turboMode ? 300 : 1000);
                            }
                        }
                    }
                    break;
                }

                case 'exploding': {
                    timerDelay -= dt;
                    let particlesTriggered = false;

                    // Winning highlight pulse & shrink animation
                    for (let r = 0; r < gridRows; r++) {
                        for (let c = 0; c < gridCols; c++) {
                            let sym = grid[r][c];
                            if (sym && sym.isExploding) {
                                // If we are in the initial pulse stage (first 700ms), pulse scale
                                if (timerDelay > (turboMode ? 80 : 300)) {
                                    let pulsePhase = timerDelay * 0.015;
                                    sym.explodeScale = 1.0 + Math.sin(pulsePhase) * 0.12;
                                } else {
                                    // Settle and shrink
                                    sym.explodeScale *= 0.8;
                                    
                                    // Trigger pops and particles at the exact frame of shrinkage
                                    if (!sym.particlesSpawned) {
                                        sym.particlesSpawned = true;
                                        let colColors = { 'star':'#ff4500', 'puffer':'#00f3ff', 'clam':'#9d00ff', 'octopus':'#ff00aa', 'angler':'#39ff14', 'blue_jelly':'#00f3ff', 'pink_jelly':'#ff007f', 'gold_jelly':'#ffd700'};
                                        spawnClusterExplosion(sym.x, sym.y, colColors[sym.type] || '#ffffff');
                                        playSound('pop', { pitch: 500 + (r * 30) });
                                    }
                                }
                            } else if (sym) {
                                updateSoftBodyWobble(sym, dtFactor);
                            }
                        }
                    }
                    if (colossalJelly) {
                        if (colossalJelly.isExploding) {
                            if (timerDelay > (turboMode ? 80 : 300)) {
                                colossalJelly.explodeScale = 1.0 + Math.sin(timerDelay*0.015)*0.12;
                            } else {
                                colossalJelly.explodeScale *= 0.8;
                                if (!colossalJelly.particlesSpawned) {
                                    colossalJelly.particlesSpawned = true;
                                    spawnClusterExplosion(colossalJelly.x, colossalJelly.y, '#ffd700');
                                    playSound('pop', { pitch: 350 });
                                }
                            }
                        } else {
                            updateSoftBodyWobble(colossalJelly, dtFactor);
                        }
                    }

                    if (timerDelay <= 0) {
                        for (let r = 0; r < gridRows; r++) {
                            for (let c = 0; c < gridCols; c++) {
                                if (grid[r][c] && grid[r][c].isExploding) {
                                    grid[r][c] = null;
                                }
                            }
                        }
                        
                        if (colossalJelly && colossalJelly.isExploding) {
                            colossalJelly = null;
                            shadowOverlayAlpha = 0;
                            colossalSize = 2;
                            colossalMult = 2;
                            updateUIState();
                        }
                        
                        activeClusters = []; 
                        gameState = 'cascading';
                    }
                    break;
                }

                case 'cascading': {
                    for (let c = 0; c < gridCols; c++) {
                        let emptyCount = 0;
                        for (let r = gridRows - 1; r >= 0; r--) {
                            if (grid[r][c] === null) {
                                emptyCount++;
                            } else if (emptyCount > 0) {
                                let sym = grid[r][c];
                                grid[r][c] = null;
                                grid[r + emptyCount][c] = sym;
                                sym.gridY = r + emptyCount;
                                sym.targetY = gridStartY + sym.gridY * (cellWidth + gap) + cellWidth / 2;
                                sym.state = 'falling';
                            }
                        }
                        
                        for (let i = 0; i < emptyCount; i++) {
                            let targetRow = emptyCount - 1 - i;
                            let spawnY = -(i + 1) * (cellWidth + gap) - 30 - c * 40;
                            grid[targetRow][c] = spawnSymbol(c, targetRow, spawnY);
                        }
                    }
                    
                    // Added a 200ms delay after explosion pops before falling symbols begin to drop
                    timerDelay = turboMode ? 50 : 100;
                    gameState = 'falling';
                    break;
                }

                case 'colossal_intro': {
                    shadowOverlayAlpha += (0.8 - shadowOverlayAlpha) * 0.08;
                    alertOverlay = { text: 'COLOSSAL JELLY DROP!', alpha: 1.0, timer: 90 };
                    
                    timerDelay -= dt;
                    if (timerDelay <= 0) {
                        gameState = 'colossal_falling';
                        
                        const S = colossalSize;
                        const maxCol = gridCols - S;
                        const maxRow = gridRows - S;
                        const sc = Math.floor(Math.random() * (maxCol + 1));
                        const sr = Math.floor(Math.random() * (maxRow + 1));

                        const targetX = gridStartX + sc * (cellWidth + gap) + (S * cellWidth + (S - 1) * gap) / 2;
                        const targetY = gridStartY + sr * (cellWidth + gap) + (S * cellWidth + (S - 1) * gap) / 2;

                        const convertTypes = ['star', 'puffer', 'clam', 'octopus', 'angler'];
                        colossalSymbolToConvert = convertTypes[Math.floor(Math.random() * convertTypes.length)];

                        colossalJelly = {
                            type: 'colossal',
                            size: S,
                            gridX: sc,
                            gridY: sr,
                            x: targetX,
                            y: -250,
                            targetY: targetY,
                            vy: 0,
                            scaleX: 1.0,
                            scaleY: 1.0,
                            bounceVel: 0,
                            multiplier: colossalMult,
                            state: 'falling',
                            isColossal: true,
                            isExploding: false,
                            explodeScale: 1.0
                        };

                        playSound('spin');
                    }
                    break;
                }

                case 'colossal_falling': {
                    colossalReticleAlpha += (0.6 - colossalReticleAlpha) * 0.1 * dtFactor;
                    
                    const cGrav = turboMode ? 1.4 : 0.75;
                    const cDrag = turboMode ? 0.90 : 0.95;
                    colossalJelly.vy = colossalJelly.vy * Math.pow(cDrag, dtFactor) + cGrav * dtFactor;
                    colossalJelly.y += colossalJelly.vy * dtFactor;
                    
                    // Spawn a massive golden bubble wake behind the falling colossal jellyfish!
                    if (Math.random() < 0.45 * dtFactor) {
                        particles.push({
                            x: colossalJelly.x + (Math.random() - 0.5) * 80,
                            y: colossalJelly.y + colossalJelly.size * 10,
                            vx: (Math.random() - 0.5) * 1.5,
                            vy: colossalJelly.vy * 0.3,
                            r: 2 + Math.random() * 4,
                            color: 'rgba(255, 215, 0, 0.4)',
                            type: 'bubble',
                            life: 0,
                            maxLife: 45
                        });
                    }
                    
                    if (colossalJelly.y >= colossalJelly.targetY) {
                        colossalJelly.y = colossalJelly.targetY;
                        colossalJelly.vy = 0;
                        colossalJelly.state = 'resting';
                        colossalJelly.bounceVel = -0.52; // colossal crash bounce
                        
                        gameState = 'colossal_impact';
                        timerDelay = turboMode ? 100 : 400;
                    }
                    break;
                }

                case 'colossal_impact': {
                    playSound('colossal_impact');
                    shakeIntensity = 18; // Soft colossal screen shake rumble
                    colossalReticleAlpha = 0;

                    shockwaves.push({
                        x: colossalJelly.x,
                        y: colossalJelly.y,
                        radius: 20,
                        maxRadius: 420,
                        speed: turboMode ? 17 : 10,
                        alpha: 1.0,
                        width: 18
                    });

                    const sr2 = colossalJelly.gridY;
                    const sc2 = colossalJelly.gridX;
                    const S2 = colossalJelly.size;
                    
                    for (let r = sr2; r < sr2 + S2; r++) {
                        for (let c = sc2; c < sc2 + S2; c++) {
                            if (grid[r][c] && !grid[r][c].isColossal) {
                                spawnClusterExplosion(grid[r][c].x, grid[r][c].y, '#00f3ff');
                                grid[r][c] = null;
                            }
                            grid[r][c] = colossalJelly; 
                        }
                    }

                    gameState = 'colossal_pay';
                    break;
                }

                case 'colossal_pay': {
                    updateSoftBodyWobble(colossalJelly, dtFactor);
                    gameState = 'check_wins'; 
                    break;
                }

                case 'idle': {
                    for (let r = 0; r < gridRows; r++) {
                        for (let c = 0; c < gridCols; c++) {
                            let sym = grid[r][c];
                            if (sym) updateSoftBodyWobble(sym, dtFactor);
                        }
                    }
                    if (colossalJelly) updateSoftBodyWobble(colossalJelly, dtFactor);
                    shadowOverlayAlpha += (0 - shadowOverlayAlpha) * 0.05;
                    break;
                }
            }
            updateUIState();
        }

        function updateSoftBodyWobble(sym, dtFactor) {
            // rubby bouncy responsive spring wobble
            const stiffness = 0.07;
            const damping = 0.14;
            
            let force = -stiffness * (sym.scaleY - 1.0);
            let damp = -damping * sym.bounceVel;
            let acc = force + damp;
            
            sym.bounceVel += acc * dtFactor;
            sym.scaleY += sym.bounceVel * dtFactor;
            sym.scaleX = 2.0 - sym.scaleY; 

            if (sym.state === 'resting' && Math.abs(sym.scaleY - 1.0) < 0.002 && Math.abs(sym.bounceVel) < 0.002) {
                sym.scaleY = 1.0;
                sym.scaleX = 1.0;
                sym.bounceVel = 0;
            }
        }


        // --- RENDERING VIEWS ENGINE ---
        function render(time) {
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // Shimmery background caustics
            ctx.save();
            ctx.globalCompositeOperation = 'screen';
            ctx.fillStyle = 'rgba(0, 243, 255, 0.03)';
            for (let i = 0; i < 4; i++) {
                let rayX = (canvas.width / 4) * i + Math.sin(time * 0.0006 + i) * 35;
                let w1 = 35 + Math.sin(time * 0.0012 + i) * 15;
                let w2 = 110 + Math.sin(time * 0.0006 + i) * 35;
                
                ctx.beginPath();
                ctx.moveTo(rayX - w1, -10);
                ctx.lineTo(rayX + w1, -10);
                ctx.lineTo(rayX + w2 + 80, canvas.height + 10);
                ctx.lineTo(rayX - w2 - 80, canvas.height + 10);
                ctx.closePath();
                ctx.fill();
            }
            ctx.restore();

            // Background silhouettes (whale/shark gliding slower)
            for (let bg of bgCreatures) {
                ctx.save();
                ctx.fillStyle = 'rgba(10, 25, 42, 0.22)';
                ctx.translate(bg.x, bg.y);
                ctx.scale(bg.scaleX, 1);
                
                ctx.beginPath();
                if (bg.type === 'whale') {
                    ctx.ellipse(0, 0, bg.width * 0.45, bg.height * 0.45, 0, 0, Math.PI * 2);
                    ctx.moveTo(-bg.width * 0.4, 0);
                    ctx.quadraticCurveTo(-bg.width * 0.7, -bg.height * 0.2, -bg.width * 0.75, -bg.height * 0.35);
                    ctx.lineTo(-bg.width * 0.72, 0);
                    ctx.lineTo(-bg.width * 0.75, bg.height * 0.35);
                    ctx.quadraticCurveTo(-bg.width * 0.7, bg.height * 0.2, -bg.width * 0.4, 0);
                } else {
                    ctx.ellipse(0, 0, bg.width * 0.45, bg.height * 0.4, 0, 0, Math.PI * 2);
                    ctx.moveTo(-bg.width * 0.4, 0);
                    ctx.lineTo(-bg.width * 0.65, -bg.height * 0.5);
                    ctx.lineTo(-bg.width * 0.55, 0);
                    ctx.lineTo(-bg.width * 0.65, bg.height * 0.5);
                    ctx.closePath();
                    ctx.moveTo(-bg.width * 0.05, -bg.height * 0.3);
                    ctx.quadraticCurveTo(-bg.width * 0.1, -bg.height * 0.75, -bg.width * 0.2, -bg.height * 0.85);
                    ctx.quadraticCurveTo(-bg.width * 0.22, -bg.height * 0.5, -bg.width * 0.25, -bg.height * 0.25);
                }
                ctx.closePath();
                ctx.fill();
                ctx.restore();
            }

            // Drifting bubbles
            for (let b of bubbles) {
                ctx.save();
                ctx.globalAlpha = b.opacity;
                ctx.strokeStyle = '#ffffff';
                ctx.lineWidth = 0.8;
                ctx.beginPath();
                ctx.arc(b.x, b.y, b.r, 0, Math.PI * 2);
                ctx.stroke();
                ctx.restore();
            }

            // Drifting background plankton/sparks
            for (let p of bgPlankton) {
                ctx.save();
                ctx.globalAlpha = p.opacity;
                ctx.fillStyle = '#00f3ff';
                ctx.shadowBlur = 8;
                ctx.shadowColor = '#00f3ff';
                ctx.beginPath();
                ctx.arc(p.x, p.y, p.r, 0, Math.PI*2);
                ctx.fill();
                ctx.restore();
            }

            // Draw glowing metallic bezel frame around canvas
            ctx.save();
            ctx.strokeStyle = '#1a2c38';
            ctx.lineWidth = 10;
            ctx.strokeRect(5, 5, canvas.width - 10, canvas.height - 10);
            
            // Side light tube glows
            ctx.lineWidth = 2.5;
            ctx.shadowBlur = 12;
            ctx.strokeStyle = '#00f3ff';
            ctx.shadowColor = '#00f3ff';
            ctx.beginPath();
            ctx.moveTo(11, 10);
            ctx.lineTo(11, canvas.height - 10);
            ctx.stroke();
            
            ctx.strokeStyle = '#ff007f';
            ctx.shadowColor = '#ff007f';
            ctx.beginPath();
            ctx.moveTo(canvas.width - 11, 10);
            ctx.lineTo(canvas.width - 11, canvas.height - 10);
            ctx.stroke();
            ctx.restore();

            // Translate screenshake offsets
            ctx.save();
            if (shakeIntensity > 0.1) {
                let dx = (Math.random() * 2 - 1) * shakeIntensity;
                let dy = (Math.random() * 2 - 1) * shakeIntensity;
                ctx.translate(dx, dy);
            }

            // Draw grid slots
            for (let r = 0; r < gridRows; r++) {
                for (let c = 0; c < gridCols; c++) {
                    let cx = gridStartX + c * (cellWidth + gap);
                    let cy = gridStartY + r * (cellWidth + gap);
                    ctx.save();
                    ctx.fillStyle = '#0a141d';
                    ctx.strokeStyle = '#122330';
                    ctx.lineWidth = 1.5;
                    ctx.beginPath();
                    ctx.roundRect(cx, cy, cellWidth, cellWidth, 6);
                    ctx.fill();
                    ctx.stroke();
                    ctx.restore();
                }
            }

            // Anticipation Glowing Border highlights
            if (anticipationActive) {
                ctx.save();
                ctx.strokeStyle = `rgba(255, 0, 127, ${0.45 + Math.sin(time * 0.015) * 0.35})`;
                ctx.lineWidth = 3.5;
                ctx.shadowBlur = 20;
                ctx.shadowColor = '#ff007f';
                ctx.strokeRect(gridStartX - 4, gridStartY - 4, gridCols * (cellWidth + gap) - gap + 8, gridRows * (cellWidth + gap) - gap + 8);
                ctx.restore();
            }

            // Dark vignette overlay
            if (shadowOverlayAlpha > 0.01) {
                ctx.save();
                ctx.fillStyle = `rgba(3, 8, 14, ${shadowOverlayAlpha})`;
                ctx.fillRect(gridStartX - 5, gridStartY - 5, gridCols * (cellWidth + gap) - gap + 10, gridRows * (cellWidth + gap) - gap + 10);
                ctx.restore();
            }

            // Landing reticle for colossal jellyfish
            if (colossalJelly && colossalJelly.state === 'falling' && colossalReticleAlpha > 0.01) {
                ctx.save();
                ctx.globalAlpha = colossalReticleAlpha * (0.8 + Math.sin(time * 0.01) * 0.2);
                ctx.strokeStyle = '#ffd700';
                ctx.lineWidth = 2.5;
                ctx.shadowBlur = 20;
                ctx.shadowColor = '#ffd700';
                
                const S = colossalJelly.size;
                const rx = gridStartX + colossalJelly.gridX * (cellWidth + gap);
                const ry = gridStartY + colossalJelly.gridY * (cellWidth + gap);
                const rSize = S * cellWidth + (S - 1) * gap;
                ctx.strokeRect(rx, ry, rSize, rSize);
                
                ctx.beginPath();
                ctx.moveTo(rx + rSize/2, ry - 12);
                ctx.lineTo(rx + rSize/2, ry + rSize + 12);
                ctx.moveTo(rx - 12, ry + rSize/2);
                ctx.lineTo(rx + rSize + 12, ry + rSize/2);
                ctx.stroke();
                
                ctx.fillStyle = '#ffffff';
                ctx.shadowBlur = 0;
                ctx.font = '800 11px "Outfit", sans-serif';
                ctx.textAlign = 'center';
                ctx.fillText(`CONVERTING: ${colossalSymbolToConvert.toUpperCase()}`, rx + rSize/2, ry + rSize/2);
                ctx.restore();
            }

            // Render ELECTRIC lightning-like arcs for connections
            if (gameState === 'exploding' && activeClusters.length > 0) {
                ctx.save();
                for (let cl of activeClusters) {
                    let baseType = cl.type;
                    let cells = cl.cells;
                    let colorMap = { 'star':'#ff4500', 'puffer':'#00f3ff', 'clam':'#9d00ff', 'octopus':'#ff00aa', 'angler':'#39ff14', 'colossal':'#ffd700' };
                    let color = colorMap[baseType] || '#ffffff';
                    
                    for (let cell1 of cells) {
                        let sym1 = grid[cell1.r][cell1.c];
                        if (!sym1) continue;
                        for (let cell2 of cells) {
                            let sym2 = grid[cell2.r][cell2.c];
                            if (!sym2 || sym1 === sym2) continue;
                            
                            let dRow = Math.abs(cell1.r - cell2.r);
                            let dCol = Math.abs(cell1.c - cell2.c);
                            if ((dRow === 1 && dCol === 0) || (dRow === 0 && dCol === 1)) {
                                let mx1 = sym1.x;
                                let my1 = sym1.y;
                                let mx2 = sym2.x;
                                let my2 = sym2.y;
                                
                                let dx = (mx2 - mx1) / 4;
                                let dy = (my2 - my1) / 4;
                                
                                ctx.strokeStyle = color;
                                ctx.lineWidth = 5.0 + Math.sin(time*0.35)*2.0;
                                ctx.shadowBlur = 20;
                                ctx.shadowColor = color;
                                ctx.globalAlpha = 0.55;
                                
                                ctx.beginPath();
                                ctx.moveTo(mx1, my1);
                                for (let step = 1; step < 4; step++) {
                                    let px = mx1 + dx * step + (Math.random() - 0.5) * 7;
                                    let py = my1 + dy * step + (Math.random() - 0.5) * 7;
                                    ctx.lineTo(px, py);
                                }
                                ctx.lineTo(mx2, my2);
                                ctx.stroke();
                                
                                ctx.strokeStyle = '#ffffff';
                                ctx.lineWidth = 1.5;
                                ctx.shadowBlur = 0;
                                ctx.globalAlpha = 1.0;
                                ctx.beginPath();
                                ctx.moveTo(mx1, my1);
                                for (let step = 1; step < 4; step++) {
                                    let px = mx1 + dx * step + (Math.random() - 0.5) * 4;
                                    let py = my1 + dy * step + (Math.random() - 0.5) * 4;
                                    ctx.lineTo(px, py);
                                }
                                ctx.lineTo(mx2, my2);
                                ctx.stroke();
                            }
                        }
                    }
                }
                ctx.restore();
            }

            // Render symbols
            let wavePhase = time * 0.0012; // Extremely slow wave phase for slow, calm breathing
            
            for (let r = 0; r < gridRows; r++) {
                for (let c = 0; c < gridCols; c++) {
                    let sym = grid[r][c];
                    if (sym && !sym.isColossal) {
                        let scale = sym.isExploding ? sym.explodeScale : 1.0;
                        
                        let finalScaleX = sym.scaleX * scale;
                        let finalScaleY = sym.scaleY * scale;
                        let finalPhase = wavePhase + r * 0.35 + c * 0.25;
                        
                        if (sym.state === 'resting' && !sym.isExploding) {
                            // Hypnotizing slow breathing (frequency 0.0008, approx. 8 seconds cycle)
                            let breathe = Math.sin(time * 0.0008 + r * 0.5 + c * 0.35);
                            finalScaleX *= (1.0 + breathe * 0.08);
                            finalScaleY *= (1.0 - breathe * 0.08);
                            
                            // Subtle rhythmic swaying phase offset
                            finalPhase += Math.cos(time * 0.0006 + r * 0.4 + c * 0.2) * 0.20;
                        }
                        
                        ctx.save();
                        ctx.translate(sym.x, sym.y);
                        ctx.scale(finalScaleX, finalScaleY);
                        if (sym.opacity !== undefined) {
                            ctx.globalAlpha = sym.opacity;
                        }
                        
                        if (sym.type === 'star') {
                            drawStarfish(ctx, 0, 0, 20, finalPhase);
                        } else if (sym.type === 'puffer') {
                            drawPufferfish(ctx, 0, 0, 20, finalPhase);
                        } else if (sym.type === 'clam') {
                            drawClam(ctx, 0, 0, 20, finalPhase);
                        } else if (sym.type === 'octopus') {
                            drawOctopus(ctx, 0, 0, 20, finalPhase);
                        } else if (sym.type === 'angler') {
                            drawAnglerfish(ctx, 0, 0, 20, finalPhase);
                        } else if (sym.type === 'blue_jelly') {
                            drawUpgradeJelly(ctx, 0, 0, 20, finalPhase, 1, 1, 'blue');
                        } else if (sym.type === 'pink_jelly') {
                            drawUpgradeJelly(ctx, 0, 0, 20, finalPhase, 1, 1, 'pink');
                        } else if (sym.type === 'gold_jelly') {
                            drawGoldScatterJelly(ctx, 0, 0, 20, finalPhase, 1, 1);
                        }
                        
                        ctx.restore();
                    }
                }
            }

            // Draw Colossal Jellyfish
            if (colossalJelly) {
                let scale = colossalJelly.isExploding ? colossalJelly.explodeScale : 1.0;
                
                if (colossalJelly.state === 'resting') {
                    ctx.save();
                    const S = colossalJelly.size;
                    const rx = gridStartX + colossalJelly.gridX * (cellWidth + gap);
                    const ry = gridStartY + colossalJelly.gridY * (cellWidth + gap);
                    const rSize = S * cellWidth + (S - 1) * gap;
                    
                    let convertedColors = {
                        'star': 'rgba(255, 69, 0, 0.12)',
                        'puffer': 'rgba(0, 243, 255, 0.12)',
                        'clam': 'rgba(157, 0, 255, 0.12)',
                        'octopus': 'rgba(255, 0, 170, 0.12)',
                        'angler': 'rgba(57, 255, 20, 0.12)'
                    };
                    ctx.fillStyle = convertedColors[colossalSymbolToConvert] || 'rgba(255, 215, 0, 0.15)';
                    ctx.strokeStyle = '#ffd700';
                    ctx.lineWidth = 1.5;
                    ctx.shadowBlur = 10;
                    ctx.shadowColor = '#ffd700';
                    
                    ctx.beginPath();
                    ctx.roundRect(rx, ry, rSize, rSize, 12);
                    ctx.fill();
                    ctx.stroke();
                    ctx.restore();
                }

                let finalColScaleX = colossalJelly.scaleX * scale;
                let finalColScaleY = colossalJelly.scaleY * scale;
                let finalColPhase = wavePhase * 0.8;

                if (colossalJelly.state === 'resting' && !colossalJelly.isExploding) {
                    let colBreathe = Math.sin(time * 0.001);
                    finalColScaleX *= (1.0 + colBreathe * 0.05);
                    finalColScaleY *= (1.0 - colBreathe * 0.05);
                    finalColPhase += Math.cos(time * 0.0008) * 0.15;
                }

                ctx.save();
                if (colossalJelly.opacity !== undefined) {
                    ctx.globalAlpha = colossalJelly.opacity;
                }
                drawColossalJellyfish(
                    ctx,
                    colossalJelly.x,
                    colossalJelly.y,
                    colossalJelly.size * 25, 
                    finalColPhase,
                    finalColScaleX,
                    finalColScaleY,
                    colossalJelly.multiplier
                );
                ctx.restore();
            }

            // Render Particles & Shockwaves inside the screenshake
            updateAndDrawShockwaves();
            updateAndDrawParticles();
            updateAndDrawFloatingTexts();

            ctx.restore();

            // Draw progressive bar HUD
            drawProgressiveHUD();

            // Win celebrations
            drawWinCelebrationOverlay(time);
            drawAlertOverlay();
        }

        // HUD progressive meter
        function drawProgressiveHUD() {
            const barX = gridStartX;
            const barY = 32;
            const barW = gridCols * (cellWidth + gap) - gap;
            const barH = 14;
            
            ctx.save();
            ctx.fillStyle = '#0a131b';
            ctx.strokeStyle = 'rgba(255, 255, 255, 0.05)';
            ctx.lineWidth = 1;
            ctx.beginPath();
            ctx.roundRect(barX, barY, barW, barH, 7);
            ctx.fill();
            ctx.stroke();

            if (currentProgress > 0) {
                let progressGrad = ctx.createLinearGradient(barX, 0, barX + barW, 0);
                progressGrad.addColorStop(0, '#00f3ff');
                progressGrad.addColorStop(0.5, '#ff007f');
                progressGrad.addColorStop(1.0, '#ffd700');
                
                ctx.fillStyle = progressGrad;
                ctx.shadowBlur = 15;
                ctx.shadowColor = currentProgress >= 100 ? '#ffd700' : '#ff007f';
                ctx.beginPath();
                ctx.roundRect(barX, barY, barW * (currentProgress / 100), barH, 7);
                ctx.fill();
            }
            
            ctx.fillStyle = '#8a9db0';
            ctx.shadowBlur = 0;
            ctx.font = '800 10px "Outfit", sans-serif';
            ctx.textAlign = 'left';
            ctx.textBaseline = 'middle';
            ctx.fillText('COLOSSAL PROGRESS', barX + 8, barY + barH/2);
            
            ctx.textAlign = 'right';
            ctx.fillStyle = currentProgress >= 100 ? '#ffd700' : '#ffffff';
            ctx.font = '800 11px "Outfit", sans-serif';
            ctx.fillText(currentProgress >= 100 ? 'DROP READY!' : `${Math.floor(currentProgress)}%`, barX + barW - 8, barY + barH/2);
            ctx.restore();
        }

        function drawWinCelebrationOverlay(time) {
            if (winCelebration.timer <= 0) return;
            winCelebration.timer--;
            
            if (winCelebration.timer > 100) {
                winCelebration.scale += (1.0 - winCelebration.scale) * 0.15;
            } else if (winCelebration.timer < 20) {
                winCelebration.scale += (0.0 - winCelebration.scale) * 0.15;
            }

            ctx.save();
            ctx.globalAlpha = Math.min(1.0, winCelebration.timer / 15);
            
            let spotlight = ctx.createRadialGradient(canvas.width/2, canvas.height/2, 20, canvas.width/2, canvas.height/2, 280);
            spotlight.addColorStop(0, 'rgba(15, 33, 46, 0.88)');
            spotlight.addColorStop(1, 'rgba(15, 33, 46, 0.0)');
            ctx.fillStyle = spotlight;
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            ctx.translate(canvas.width/2, canvas.height/2 - 20);
            ctx.scale(winCelebration.scale, winCelebration.scale);

            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            ctx.font = '800 36px "Outfit", sans-serif';
            
            let colors = ['#ffd700', '#ff007f', '#00f3ff'];
            let chosenColor = colors[Math.floor(time / 180) % colors.length];
            
            ctx.shadowBlur = 25;
            ctx.shadowColor = chosenColor;
            ctx.fillStyle = '#ffffff';
            ctx.fillText(winCelebration.text, 0, -25);
            
            ctx.fillStyle = '#00e701';
            ctx.shadowColor = '#00e701';
            ctx.font = '800 48px "Outfit", sans-serif';
            ctx.fillText(`+$${winCelebration.winAmt.toFixed(2)}`, 0, 30);
            ctx.restore();
        }

        function drawAlertOverlay() {
            if (alertOverlay.timer <= 0) return;
            alertOverlay.timer--;

            if (alertOverlay.timer < 15) {
                alertOverlay.alpha = alertOverlay.timer / 15;
            } else {
                alertOverlay.alpha = Math.min(1.0, (90 - alertOverlay.timer) / 8);
            }

            ctx.save();
            ctx.globalAlpha = alertOverlay.alpha;
            ctx.fillStyle = 'rgba(0, 243, 255, 0.05)';
            ctx.fillRect(0, canvas.height/2 - 50, canvas.width, 100);
            
            ctx.strokeStyle = '#00f3ff';
            ctx.lineWidth = 2;
            ctx.shadowBlur = 15;
            ctx.shadowColor = '#00f3ff';
            ctx.beginPath();
            ctx.moveTo(0, canvas.height/2 - 50);
            ctx.lineTo(canvas.width, canvas.height/2 - 50);
            ctx.moveTo(0, canvas.height/2 + 50);
            ctx.lineTo(canvas.width, canvas.height/2 + 50);
            ctx.stroke();

            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            ctx.font = '800 22px "Outfit", sans-serif';
            ctx.fillStyle = '#ffffff';
            ctx.fillText(alertOverlay.text, canvas.width/2, canvas.height/2);
            ctx.restore();
        }

        // --- TICK TIMING FRAME LOOP ---
        function tick(time) {
            update(time);
            render(time);
            requestAnimationFrame(tick);
        }
        
        requestAnimationFrame(tick);

    </script>
</body>
</html>
"""

# Render the upgraded game inside Streamlit frame
components.html(html_code, height=920, scrolling=False)
