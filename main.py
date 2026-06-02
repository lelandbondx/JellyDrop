import streamlit as st
import streamlit.components.v1 as components

# Set up page configurations
st.set_page_config(
    page_title="Jelly Drop | Stake Originals",
    page_icon="🪼",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS to hide Streamlit components and force dark Stake Slate theme
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

# Main Game embedded payload
html_code = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Jelly Drop</title>
    <!-- Outfit Font for clean, premium styling -->
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
            font-size: 24px;
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
        #sound-notification {
            position: absolute;
            top: 90px;
            left: 50%;
            transform: translateX(-50%);
            background: rgba(255, 215, 0, 0.9);
            color: #000000;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 800;
            z-index: 100;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.5);
            pointer-events: none;
            transition: opacity 0.5s, transform 0.5s;
            opacity: 0;
            transform: translate(-50%, -20px);
        }
        #sound-notification.visible {
            opacity: 1;
            transform: translate(-50%, 0);
        }

        /* Canvas game viewport */
        #canvas-container {
            position: relative;
            width: 100%;
            height: 640px;
            background: radial-gradient(circle at center, #0e2230 0%, #060b10 100%);
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
            background: rgba(15, 33, 46, 0.96);
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
        .btn-bet:active:not(:disabled) {
            background: #1e2c38;
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
        
        /* Audio Enable Overlay screen (Crucial for browser autoplay bypass) */
        #audio-overlay {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(11, 22, 32, 0.95);
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
            font-size: 48px;
            font-weight: 800;
            letter-spacing: 4px;
            background: linear-gradient(45deg, #00f3ff, #ff007f);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 20px;
            filter: drop-shadow(0 0 15px rgba(0, 243, 255, 0.4));
        }
        .overlay-text {
            font-size: 16px;
            color: #8a9db0;
            margin-bottom: 30px;
            line-height: 1.6;
            max-width: 320px;
        }
        .btn-start {
            background: linear-gradient(90deg, #00f3ff, #ff007f);
            color: #ffffff;
            border: none;
            outline: none;
            font-family: 'Outfit', sans-serif;
            font-weight: 800;
            font-size: 18px;
            padding: 14px 40px;
            border-radius: 30px;
            cursor: pointer;
            box-shadow: 0 0 25px rgba(0, 243, 255, 0.4);
            transition: transform 0.2s, box-shadow 0.2s;
        }
        .btn-start:hover {
            transform: scale(1.05);
            box-shadow: 0 0 35px rgba(255, 0, 127, 0.6);
        }
        .btn-start:active {
            transform: scale(0.98);
        }
    </style>
</head>
<body>

    <div id="game-wrapper">
        <!-- Interactive Overlay to bypass Autoplay blocks & activate Web Audio API -->
        <div id="audio-overlay">
            <div class="overlay-logo">JELLY DROP</div>
            <div class="overlay-text">
                Prepare for a high-volatility underwater cluster-pay casino experience. Click below to enable dynamic bioluminescent sounds.
            </div>
            <button class="btn-start" onclick="startGame()">ENTER DEEP SEA</button>
        </div>

        <div id="sound-notification">SOUNDS ENABLED - VOLUME AT 100%</div>

        <!-- Upper Board Header -->
        <div id="game-header">
            <div id="logo-container">
                <h1 id="game-title">JELLY DROP</h1>
                <div id="game-subtitle">Biomagnetic Paylines</div>
            </div>
            
            <div class="display-box text-right" style="min-width: 140px; background: transparent; border: none; padding: 0;">
                <span class="label" style="font-size: 9px; letter-spacing: 2px;">progressive bonus</span>
                <div style="font-size: 15px; font-weight: 800; color: #ffd700; text-shadow: 0 0 8px rgba(255, 215, 0, 0.4);" id="progressive-percentage">0% CHARGED</div>
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

                <button id="spin-button" class="btn-spin" onclick="triggerSpin()">SPIN</button>

                <div class="toggle-controls">
                    <!-- Turbo Mode Toggle -->
                    <button class="btn-icon" id="btn-turbo" onclick="toggleTurbo()" title="Turbo Mode (Faster drops)">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>
                    </button>
                    <!-- Auto Spin Toggle -->
                    <button class="btn-icon" id="btn-auto" onclick="toggleAuto()" title="Auto Spin Mode">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M21.5 2v6h-6M21.34 15.57a10 10 0 1 1-.57-8.38l5.67-5.67"/></svg>
                    </button>
                    <!-- Audio Mute Toggle -->
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

        // Game parameters
        const gridCols = 7;
        const gridRows = 7;
        const cellWidth = 60;
        const gap = 8;
        const gridStartX = 66; // Horizontally center: (600 - (7*60 + 6*8))/2 = 66
        const gridStartY = 95;  // Start slightly down inside canvas

        // Volatility multipliers & payouts
        const payouts = {
            'cyan': 0.1,    // Neon Cyan
            'magenta': 0.2, // Electric Magenta
            'green': 0.4,   // Toxic Green
            'purple': 0.7,  // Deep Purple
            'gold': 1.5     // Radiant Gold (Highest Base)
        };

        // State Machine
        let gameState = 'idle'; // idle, clearing_prev, falling, check_wins, exploding, cascading, colossal_intro, colossal_falling, colossal_impact, colossal_pay, colossal_exploding
        let grid = Array(gridRows).fill(null).map(() => Array(gridCols).fill(null));
        let balance = 1000.00;
        let betAmount = 1.00;
        let spinWin = 0.00;
        let progressiveProgress = 0; // 0 to 100
        let currentProgress = 0; // smooth tracking of progressive bar
        let turboMode = false;
        let autoSpin = false;
        let isMuted = false;

        // Particle systems & visual FX
        let particles = [];
        let shockwaves = [];
        let floatingTexts = [];
        let bubbles = [];
        let shakeIntensity = 0;
        let shadowOverlayAlpha = 0;
        let alertOverlay = { text: '', alpha: 0, timer: 0 };
        let winCelebration = { text: '', winAmt: 0, timer: 0, scale: 0 };
        let timerDelay = 0;
        let colossalJelly = null;
        let colossalReticleAlpha = 0;

        // Sound Synthesis (Web Audio API)
        let audioCtx = null;
        let ambientOsc = null;
        let ambientGain = null;

        // Time trackers
        let lastTime = 0;
        let cycleTime = 0;

        // Initialize background bubbles
        for (let i = 0; i < 25; i++) {
            bubbles.push({
                x: Math.random() * canvas.width,
                y: Math.random() * canvas.height + canvas.height,
                vx: 0,
                vy: -0.5 - Math.random() * 1.5,
                r: 1 + Math.random() * 4,
                wobbleSpeed: 0.02 + Math.random() * 0.03,
                wobbleAmt: 2 + Math.random() * 4,
                opacity: 0.1 + Math.random() * 0.3
            });
        }

        // --- WEB AUDIO ENGINE (Procedural Audio Synthesis) ---
        function initAudio() {
            if (audioCtx) return;
            try {
                audioCtx = new (window.AudioContext || window.webkitAudioContext)();
                
                // Deep-sea rumble hum
                ambientOsc = audioCtx.createOscillator();
                let filter = audioCtx.createBiquadFilter();
                ambientGain = audioCtx.createGain();
                
                ambientOsc.type = 'triangle';
                ambientOsc.frequency.value = 48; // Deep Sub rumble
                
                filter.type = 'lowpass';
                filter.frequency.value = 90;
                
                ambientGain.gain.value = isMuted ? 0 : 0.22;
                
                // LFO to create water wave swell effect
                let lfo = audioCtx.createOscillator();
                let lfoGain = audioCtx.createGain();
                lfo.frequency.value = 0.15; // 6-7 second wave
                lfoGain.gain.value = 0.06;
                
                lfo.connect(lfoGain);
                lfoGain.connect(ambientGain.gain);
                
                ambientOsc.connect(filter);
                filter.connect(ambientGain);
                ambientGain.connect(audioCtx.destination);
                
                lfo.start();
                ambientOsc.start();
            } catch(e) {
                console.error("Audio Context initialization failed", e);
            }
        }

        function playSound(type, options = {}) {
            if (!audioCtx || isMuted) return;
            try {
                let now = audioCtx.currentTime;
                
                if (type === 'spin') {
                    // Synth whoosh
                    let osc = audioCtx.createOscillator();
                    let filter = audioCtx.createBiquadFilter();
                    let gain = audioCtx.createGain();
                    
                    osc.type = 'sine';
                    osc.frequency.setValueAtTime(350, now);
                    osc.frequency.exponentialRampToValueAtTime(70, now + 0.4);
                    
                    filter.type = 'lowpass';
                    filter.frequency.setValueAtTime(250, now);
                    filter.frequency.exponentialRampToValueAtTime(60, now + 0.4);
                    
                    gain.gain.setValueAtTime(0.18, now);
                    gain.gain.exponentialRampToValueAtTime(0.001, now + 0.4);
                    
                    osc.connect(filter);
                    filter.connect(gain);
                    gain.connect(audioCtx.destination);
                    
                    osc.start(now);
                    osc.stop(now + 0.4);
                }
                
                else if (type === 'impact') {
                    // Soft thud landing
                    let osc = audioCtx.createOscillator();
                    let gain = audioCtx.createGain();
                    
                    osc.type = 'triangle';
                    osc.frequency.setValueAtTime(110, now);
                    osc.frequency.exponentialRampToValueAtTime(30, now + 0.18);
                    
                    gain.gain.setValueAtTime(0.15, now);
                    gain.gain.exponentialRampToValueAtTime(0.001, now + 0.18);
                    
                    osc.connect(gain);
                    gain.connect(audioCtx.destination);
                    
                    osc.start(now);
                    osc.stop(now + 0.18);
                }
                
                else if (type === 'pop') {
                    // Fast upward water bubble pop
                    let osc = audioCtx.createOscillator();
                    let gain = audioCtx.createGain();
                    
                    osc.type = 'sine';
                    // Skewed starting pitch based on cluster size to represent higher wins
                    let startPitch = options.pitch || 440;
                    osc.frequency.setValueAtTime(startPitch, now);
                    osc.frequency.exponentialRampToValueAtTime(startPitch * 2.2, now + 0.08);
                    
                    gain.gain.setValueAtTime(0.12, now);
                    gain.gain.exponentialRampToValueAtTime(0.001, now + 0.08);
                    
                    osc.connect(gain);
                    gain.connect(audioCtx.destination);
                    
                    osc.start(now);
                    osc.stop(now + 0.08);
                }
                
                else if (type === 'win_tune') {
                    // Synthesized chime arpeggio
                    let notes = [261.63, 293.66, 329.63, 392.00, 440.00, 523.25, 587.33, 659.25, 783.99]; // Pentatonic scale
                    let speed = 0.07;
                    let numNotes = Math.min(3 + Math.floor((options.multiplier || 1) * 3), 9);
                    
                    for (let i = 0; i < numNotes; i++) {
                        let note = notes[i % notes.length];
                        let noteTime = now + (i * speed);
                        
                        let osc = audioCtx.createOscillator();
                        let filter = audioCtx.createBiquadFilter();
                        let gain = audioCtx.createGain();
                        
                        osc.type = 'sine';
                        osc.frequency.setValueAtTime(note, noteTime);
                        
                        filter.type = 'lowpass';
                        filter.frequency.setValueAtTime(1500, noteTime);
                        
                        gain.gain.setValueAtTime(0.08, noteTime);
                        gain.gain.exponentialRampToValueAtTime(0.001, noteTime + 0.25);
                        
                        osc.connect(filter);
                        filter.connect(gain);
                        gain.connect(audioCtx.destination);
                        
                        osc.start(noteTime);
                        osc.stop(noteTime + 0.25);
                    }
                }
                
                else if (type === 'colossal_impact') {
                    // Dramatic low bass sub thump & filtered crash
                    // Low sub-bass
                    let subOsc = audioCtx.createOscillator();
                    let subGain = audioCtx.createGain();
                    subOsc.type = 'sine';
                    subOsc.frequency.setValueAtTime(80, now);
                    subOsc.frequency.linearRampToValueAtTime(20, now + 0.7);
                    
                    subGain.gain.setValueAtTime(0.45, now);
                    subGain.gain.exponentialRampToValueAtTime(0.001, now + 0.7);
                    
                    subOsc.connect(subGain);
                    subGain.connect(audioCtx.destination);
                    subOsc.start(now);
                    subOsc.stop(now + 0.7);
                    
                    // Filtered noise crash
                    let bufferSize = audioCtx.sampleRate * 0.6; // 0.6 seconds
                    let buffer = audioCtx.createBuffer(1, bufferSize, audioCtx.sampleRate);
                    let data = buffer.getChannelData(0);
                    for (let i = 0; i < bufferSize; i++) {
                        data[i] = Math.random() * 2 - 1;
                    }
                    
                    let noiseNode = audioCtx.createBufferSource();
                    noiseNode.buffer = buffer;
                    
                    let noiseFilter = audioCtx.createBiquadFilter();
                    noiseFilter.type = 'lowpass';
                    noiseFilter.frequency.setValueAtTime(600, now);
                    noiseFilter.frequency.exponentialRampToValueAtTime(80, now + 0.6);
                    
                    let noiseGain = audioCtx.createGain();
                    noiseGain.gain.setValueAtTime(0.3, now);
                    noiseGain.gain.exponentialRampToValueAtTime(0.001, now + 0.6);
                    
                    noiseNode.connect(noiseFilter);
                    noiseFilter.connect(noiseGain);
                    noiseGain.connect(audioCtx.destination);
                    
                    noiseNode.start(now);
                    noiseNode.stop(now + 0.6);
                }
            } catch (e) {
                console.error("Sound play failed", e);
            }
        }

        // --- GAME ACTIONS & BUTTON HANDLERS ---
        function startGame() {
            initAudio();
            const overlay = document.getElementById('audio-overlay');
            overlay.classList.add('fade-out');
            
            // Show toast notification that sound is initialized
            const toast = document.getElementById('sound-notification');
            toast.classList.add('visible');
            setTimeout(() => {
                toast.classList.remove('visible');
            }, 2500);

            // Populate initial board with falling symbols
            initGrid();
        }

        function initGrid() {
            gameState = 'falling';
            for (let c = 0; c < gridCols; c++) {
                for (let r = 0; r < gridRows; r++) {
                    grid[r][c] = spawnSymbol(c, r, -(r + 1) * 80 - 50);
                }
            }
        }

        function spawnSymbol(col, row, customY = null) {
            const types = ['cyan', 'cyan', 'cyan', 'magenta', 'magenta', 'green', 'green', 'purple', 'gold'];
            const chosenType = types[Math.floor(Math.random() * types.length)];
            
            // 5% chance of applying a base multiplier badge (x2, x3, or x5) to high tier
            let symMultiplier = 1;
            if (Math.random() < 0.07 && (chosenType === 'green' || chosenType === 'purple' || chosenType === 'gold')) {
                const multipliers = [2, 2, 3, 5];
                symMultiplier = multipliers[Math.floor(Math.random() * multipliers.length)];
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
                multiplier: symMultiplier,
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
            playSound('pop', { pitch: 300 });
        }

        function toggleTurbo() {
            turboMode = !turboMode;
            const btn = document.getElementById('btn-turbo');
            if (turboMode) {
                btn.classList.add('active');
            } else {
                btn.classList.remove('active');
            }
            playSound('pop', { pitch: 500 });
        }

        function toggleAuto() {
            autoSpin = !autoSpin;
            const btn = document.getElementById('btn-auto');
            if (autoSpin) {
                btn.classList.add('active-gold');
            } else {
                btn.classList.remove('active-gold');
            }
            playSound('pop', { pitch: 600 });
            
            // Auto start if idle
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
                    if (ambientGain) ambientGain.gain.setValueAtTime(0.22, audioCtx.currentTime);
                } else {
                    initAudio();
                }
            }
        }

        function updateUI() {
            document.getElementById('balance-display').innerText = `$${balance.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2})}`;
            document.getElementById('win-display').innerText = `$${spinWin.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2})}`;
            document.getElementById('progressive-percentage').innerText = `${Math.floor(progressiveProgress)}% CHARGED`;
            
            const spinBtn = document.getElementById('spin-button');
            if (gameState === 'idle') {
                spinBtn.innerText = 'SPIN';
                spinBtn.disabled = false;
            } else {
                spinBtn.innerText = 'SPINNING';
                spinBtn.disabled = true;
            }
        }

        function triggerSpin() {
            if (gameState !== 'idle') return;
            if (balance < betAmount) {
                // Insufficient balance: auto refill balance for testing
                balance = 1000.00;
                playSound('win_tune', { multiplier: 3 });
                alertOverlay = { text: 'BALANCE REFILLED! +$1000', alpha: 1.0, timer: 120 };
            }
            
            balance -= betAmount;
            spinWin = 0.00;
            updateUI();
            
            // Clear progressive charge if not trigger ready
            if (progressiveProgress < 100) {
                progressiveProgress = 0;
            }

            playSound('spin');
            
            // Clear current celebration & alert
            winCelebration.timer = 0;
            alertOverlay.timer = 0;

            // Trigger clearing physics: make all symbols slide off the bottom
            gameState = 'clearing_prev';
            for (let r = 0; r < gridRows; r++) {
                for (let c = 0; c < gridCols; c++) {
                    if (grid[r][c]) {
                        grid[r][c].state = 'clearing';
                        grid[r][c].vy = 2 + Math.random() * 3; // Random downward thrust
                    }
                }
            }
        }


        // --- DYNAMIC GRAPHICS PROCEDURAL RENDERERS ---
        function drawJellyfishSymbol(ctx, type, x, y, size, phase, scaleX, scaleY, multiplier) {
            let baseColor = '#00f3ff';
            let secondaryColor = '#0055aa';
            
            if (type === 'cyan') {
                baseColor = '#00f3ff';
                secondaryColor = '#0077bb';
            } else if (type === 'magenta') {
                baseColor = '#ff007f';
                secondaryColor = '#aa0055';
            } else if (type === 'green') {
                baseColor = '#39ff14';
                secondaryColor = '#00aa33';
            } else if (type === 'purple') {
                baseColor = '#9d00ff';
                secondaryColor = '#5500aa';
            } else if (type === 'gold') {
                baseColor = '#ffd700';
                secondaryColor = '#bb8800';
            }

            ctx.save();
            ctx.translate(x, y);
            ctx.scale(scaleX, scaleY);
            
            // Outer bioluminescent glow
            ctx.shadowBlur = 18;
            ctx.shadowColor = baseColor;

            // Tentacles (translucent curved lines waving)
            ctx.lineWidth = 2.0;
            ctx.strokeStyle = baseColor;
            ctx.globalAlpha = 0.55;
            
            const numTentacles = 4;
            for (let i = 0; i < numTentacles; i++) {
                let tx = -size * 0.45 + (i / (numTentacles - 1)) * size * 0.9;
                let ty = size * 0.15;
                ctx.beginPath();
                ctx.moveTo(tx, ty);
                
                let waveFreq = 0.08;
                let waveAmp = 5;
                let tentacleLen = size * 1.0;
                
                ctx.lineTo(tx, ty + 4);
                for (let yOffset = 4; yOffset < tentacleLen; yOffset += 4) {
                    let angle = phase + yOffset * waveFreq - i * 0.6;
                    let wx = tx + Math.sin(angle) * waveAmp;
                    ctx.lineTo(wx, ty + yOffset);
                }
                ctx.stroke();
            }

            ctx.globalAlpha = 1.0;

            // Draw Head Dome
            let capGrad = ctx.createRadialGradient(0, -size * 0.15, 2, 0, 0, size * 0.85);
            capGrad.addColorStop(0, '#ffffff');
            capGrad.addColorStop(0.35, baseColor);
            capGrad.addColorStop(1, secondaryColor);
            
            ctx.fillStyle = capGrad;
            ctx.beginPath();
            ctx.arc(0, -size * 0.1, size * 0.75, Math.PI, 0, false);
            // Fluted bell bottom edges
            ctx.bezierCurveTo(size * 0.4, size * 0.2, size * 0.2, size * 0.1, 0, size * 0.1);
            ctx.bezierCurveTo(-size * 0.2, size * 0.1, -size * 0.4, size * 0.2, -size * 0.75, -size * 0.1);
            ctx.closePath();
            ctx.fill();

            // Inner organ light
            ctx.beginPath();
            ctx.arc(0, -size * 0.2, size * 0.22, 0, Math.PI * 2);
            let coreGrad = ctx.createRadialGradient(0, -size * 0.2, 0, 0, -size * 0.2, size * 0.22);
            coreGrad.addColorStop(0, '#ffffff');
            coreGrad.addColorStop(1, 'transparent');
            ctx.fillStyle = coreGrad;
            ctx.fill();

            // Glowing bioluminescent tiny eyes
            ctx.fillStyle = '#ffffff';
            ctx.shadowBlur = 4;
            ctx.shadowColor = '#ffffff';
            ctx.beginPath();
            ctx.arc(-size * 0.2, -size * 0.08, 1.8, 0, Math.PI * 2);
            ctx.arc(size * 0.2, -size * 0.08, 1.8, 0, Math.PI * 2);
            ctx.fill();

            ctx.restore();
            
            // Draw Multiplier badge
            if (multiplier && multiplier > 1) {
                ctx.save();
                ctx.translate(x + size * 0.45, y - size * 0.55);
                ctx.fillStyle = '#ff0055';
                ctx.strokeStyle = '#ffffff';
                ctx.lineWidth = 1.5;
                ctx.shadowBlur = 8;
                ctx.shadowColor = '#ff0055';
                
                ctx.beginPath();
                ctx.arc(0, 0, 10, 0, Math.PI * 2);
                ctx.fill();
                ctx.stroke();
                
                ctx.fillStyle = '#ffffff';
                ctx.shadowBlur = 0;
                ctx.font = 'bold 9px "Outfit", sans-serif';
                ctx.textAlign = 'center';
                ctx.textBaseline = 'middle';
                ctx.fillText(`${multiplier}x`, 0, 0);
                ctx.restore();
            }
        }

        function drawColossalJellyfish(ctx, x, y, size, phase, scaleX, scaleY, multiplier) {
            ctx.save();
            ctx.translate(x, y);
            ctx.scale(scaleX, scaleY);
            
            let baseColor = '#ffd700'; // Pure gold glow
            
            // Hyper glow
            ctx.shadowBlur = 35;
            ctx.shadowColor = baseColor;
            
            // Heavy tentacles
            ctx.lineWidth = 5.0;
            ctx.strokeStyle = baseColor;
            ctx.globalAlpha = 0.65;
            
            const numTentacles = 8;
            for (let i = 0; i < numTentacles; i++) {
                let tx = -size * 0.5 + (i / (numTentacles - 1)) * size * 1.0;
                let ty = size * 0.12;
                ctx.beginPath();
                ctx.moveTo(tx, ty);
                
                let waveFreq = 0.04;
                let waveAmp = 12;
                let tentacleLen = size * 1.25;
                
                ctx.lineTo(tx, ty + 8);
                for (let yOffset = 8; yOffset < tentacleLen; yOffset += 6) {
                    let angle = phase + yOffset * waveFreq - i * 0.5;
                    let wx = tx + Math.sin(angle) * waveAmp;
                    ctx.lineTo(wx, ty + yOffset);
                }
                ctx.stroke();
            }

            ctx.globalAlpha = 1.0;
            
            // Giant Royal crown bell dome
            let capGrad = ctx.createRadialGradient(0, -size * 0.12, 5, 0, 0, size * 0.9);
            capGrad.addColorStop(0, '#ffffff');
            capGrad.addColorStop(0.3, baseColor);
            capGrad.addColorStop(1, '#552200');
            
            ctx.fillStyle = capGrad;
            ctx.beginPath();
            ctx.moveTo(-size * 0.85, -size * 0.08);
            ctx.bezierCurveTo(-size * 0.85, -size * 0.65, -size * 0.5, -size * 0.85, -size * 0.35, -size * 0.85);
            ctx.lineTo(-size * 0.22, -size * 0.58);
            ctx.lineTo(0, -size * 0.95); // High center crown peak
            ctx.lineTo(size * 0.22, -size * 0.58);
            ctx.lineTo(size * 0.35, -size * 0.85);
            ctx.bezierCurveTo(size * 0.5, -size * 0.85, size * 0.9, -size * 0.65, size * 0.85, -size * 0.08);
            
            // Scalloped bottom
            ctx.bezierCurveTo(size * 0.5, size * 0.22, size * 0.25, size * 0.1, 0, size * 0.1);
            ctx.bezierCurveTo(-size * 0.25, size * 0.1, -size * 0.5, size * 0.22, -size * 0.85, -size * 0.08);
            ctx.closePath();
            ctx.fill();
            
            // Giant interior core
            ctx.beginPath();
            ctx.arc(0, -size * 0.2, size * 0.32, 0, Math.PI * 2);
            let coreGrad = ctx.createRadialGradient(0, -size * 0.2, 0, 0, -size * 0.2, size * 0.32);
            coreGrad.addColorStop(0, '#ffffff');
            coreGrad.addColorStop(0.4, '#ffd700');
            coreGrad.addColorStop(1, 'transparent');
            ctx.fillStyle = coreGrad;
            ctx.fill();
            
            // Crimson peak rubies
            ctx.fillStyle = '#ff2200';
            ctx.shadowBlur = 12;
            ctx.shadowColor = '#ff2200';
            ctx.beginPath();
            ctx.arc(-size * 0.35, -size * 0.85, 4.5, 0, Math.PI * 2);
            ctx.arc(0, -size * 0.95, 5.5, 0, Math.PI * 2);
            ctx.arc(size * 0.35, -size * 0.85, 4.5, 0, Math.PI * 2);
            ctx.fill();
            
            ctx.restore();
            
            // Multiplier Badge board
            ctx.save();
            ctx.translate(x, y - 5);
            ctx.fillStyle = 'rgba(15, 33, 46, 0.92)';
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

        // --- PARTICLE ENGINE ---
        function spawnClusterExplosion(x, y, color) {
            // Spawn 30-40 vector droplets and bubbles per detonating symbol
            const count = 30 + Math.floor(Math.random() * 10);
            for (let i = 0; i < count; i++) {
                let angle = Math.random() * Math.PI * 2;
                let vel = 3 + Math.random() * 7;
                particles.push({
                    x: x,
                    y: y,
                    vx: Math.cos(angle) * vel,
                    vy: Math.sin(angle) * vel,
                    r: 2 + Math.random() * 4,
                    color: color,
                    type: Math.random() < 0.55 ? 'droplet' : 'bubble',
                    life: 0,
                    maxLife: 40 + Math.floor(Math.random() * 15) // ~800ms
                });
            }
        }

        function updateAndDrawParticles() {
            for (let i = particles.length - 1; i >= 0; i--) {
                let p = particles[i];
                p.life++;
                
                // Simulated water drag: slow down speed rapidly
                p.vx *= 0.89;
                p.vy *= 0.89;
                
                // Physics: buoyancy vs gravity
                if (p.type === 'bubble') {
                    p.vy -= 0.16; // float up like gas bubble
                } else {
                    p.vy += 0.08; // slow ink drift down
                }
                
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
                    // Vector droplet with motion tail
                    ctx.fillStyle = p.color;
                    let speed = Math.sqrt(p.vx * p.vx + p.vy * p.vy);
                    if (speed > 0.4) {
                        ctx.beginPath();
                        ctx.moveTo(p.x - p.vx * 1.5, p.y - p.vy * 1.5);
                        ctx.lineTo(p.x + p.vy * 0.3, p.y - p.vx * 0.3);
                        ctx.lineTo(p.x - p.vy * 0.3, p.y + p.vx * 0.3);
                        ctx.closePath();
                        ctx.fill();
                    }
                    ctx.beginPath();
                    ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
                    ctx.fill();
                }
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


        // --- CLUSTER RESOLVING CORE ---
        function getCluster(startRow, startCol, matchType) {
            const cluster = [];
            const queue = [{ r: startRow, c: startCol }];
            const visited = Array(gridRows).fill(null).map(() => Array(gridCols).fill(false));
            visited[startRow][startCol] = true;

            while (queue.length > 0) {
                const current = queue.shift();
                cluster.push(current);

                const directions = [
                    { r: -1, c: 0 },
                    { r: 1, c: 0 },
                    { r: 0, c: -1 },
                    { r: 0, c: 1 }
                ];

                for (let dir of directions) {
                    const nr = current.r + dir.r;
                    const nc = current.c + dir.c;

                    if (nr >= 0 && nr < gridRows && nc >= 0 && nc < gridCols) {
                        if (!visited[nr][nc] && grid[nr][nc] && !grid[nr][nc].isExploding) {
                            // Match same normal types
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

            // 1. Detect standard clusters
            for (let r = 0; r < gridRows; r++) {
                for (let c = 0; c < gridCols; c++) {
                    const sym = grid[r][c];
                    if (sym && !sym.isExploding && !visited[r][c] && !sym.isColossal) {
                        const cluster = getCluster(r, c, sym.type);
                        // Mark all elements in cluster visited
                        for (let cell of cluster) {
                            visited[cell.r][cell.c] = true;
                        }
                        if (cluster.length >= 5) {
                            allClusters.push({
                                type: sym.type,
                                cells: cluster
                            });
                        }
                    }
                }
            }

            // 2. Detect Colossal Golden Jelly matches if it exists on board
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
                // Colossal forms a cluster of its own size (e.g. S*S = 9 or 16).
                // Let's sweep the borders of the colossal block to find adjacent gold symbols.
                const colossalCells = [];
                const visitedGold = Array(gridRows).fill(null).map(() => Array(gridCols).fill(false));
                
                const S = colossalObj.size;
                const sc = colossalObj.gridX;
                const sr = colossalObj.gridY;
                
                // Add colossal grid locations
                for (let r = sr; r < sr + S; r++) {
                    for (let c = sc; c < sc + S; c++) {
                        colossalCells.push({ r: r, c: c });
                    }
                }

                // Check cells adjacent to Colossal block for Gold matching
                const goldType = 'gold';
                const goldQueue = [];
                
                // Border scan to seed adjacent Gold search
                for (let r = sr; r < sr + S; r++) {
                    // Check Left
                    if (sc - 1 >= 0 && grid[r][sc - 1] && grid[r][sc - 1].type === goldType && !grid[r][sc - 1].isExploding) {
                        if (!visitedGold[r][sc - 1]) {
                            visitedGold[r][sc - 1] = true;
                            goldQueue.push({ r: r, c: sc - 1 });
                        }
                    }
                    // Check Right
                    if (sc + S < gridCols && grid[r][sc + S] && grid[r][sc + S].type === goldType && !grid[r][sc + S].isExploding) {
                        if (!visitedGold[r][sc + S]) {
                            visitedGold[r][sc + S] = true;
                            goldQueue.push({ r: r, c: sc + S });
                        }
                    }
                }
                for (let c = sc; c < sc + S; c++) {
                    // Check Above
                    if (sr - 1 >= 0 && grid[sr - 1][c] && grid[sr - 1][c].type === goldType && !grid[sr - 1][c].isExploding) {
                        if (!visitedGold[sr - 1][c]) {
                            visitedGold[sr - 1][c] = true;
                            goldQueue.push({ r: sr - 1, c: c });
                        }
                    }
                    // Check Below
                    if (sr + S < gridRows && grid[sr + S][c] && grid[sr + S][c].type === goldType && !grid[sr + S][c].isExploding) {
                        if (!visitedGold[sr + S][c]) {
                            visitedGold[sr + S][c] = true;
                            goldQueue.push({ r: sr + S, c: c });
                        }
                    }
                }

                // Expand flood fill for outer gold cells
                while (goldQueue.length > 0) {
                    const current = goldQueue.shift();
                    colossalCells.push(current);
                    
                    const dirs = [{r:-1,c:0},{r:1,c:0},{r:0,c:-1},{r:0,c:1}];
                    for (let d of dirs) {
                        const nr = current.r + d.r;
                        const nc = current.c + d.c;
                        // Avoid bounds/inside colossal block check
                        if (nr >= 0 && nr < gridRows && nc >= 0 && nc < gridCols) {
                            const inColossal = (nr >= sr && nr < sr + S && nc >= sc && nc < sc + S);
                            if (!inColossal && !visitedGold[nr][nc] && grid[nr][nc] && grid[nr][nc].type === goldType && !grid[nr][nc].isExploding) {
                                visitedGold[nr][nc] = true;
                                goldQueue.push({ r: nr, c: nc });
                            }
                        }
                    }
                }

                // Colossal cluster is guaranteed size >= 4, so it always pays out!
                allClusters.push({
                    type: 'colossal',
                    cells: colossalCells,
                    colossalObj: colossalObj
                });
            }

            return allClusters;
        }


        // --- UPDATE PHYSICS & STATE TICK ---
        function update(time) {
            let dt = time - lastTime;
            if (dt > 100) dt = 16.67; // prevent time skipping in background tabs
            lastTime = time;

            cycleTime += dt;

            // Handle screenshake decay
            if (shakeIntensity > 0.05) {
                shakeIntensity *= 0.88;
            } else {
                shakeIntensity = 0;
            }

            // Smooth progressive bar charge
            if (currentProgress < progressiveProgress) {
                currentProgress += (progressiveProgress - currentProgress) * 0.1;
            } else if (currentProgress > progressiveProgress) {
                currentProgress += (progressiveProgress - currentProgress) * 0.1;
            }

            // Ambient background bubble drift updates
            for (let b of bubbles) {
                b.y += b.vy;
                // side to side float wobble
                b.vx = Math.sin(time * b.wobbleSpeed) * (b.wobbleAmt * 0.1);
                b.x += b.vx;
                
                if (b.y < -10) {
                    b.y = canvas.height + 20;
                    b.x = Math.random() * canvas.width;
                }
            }

            // State Machine transitions
            switch (gameState) {
                case 'clearing_prev':
                    // Verify if all elements are cleared off screen
                    let activeClear = false;
                    for (let r = 0; r < gridRows; r++) {
                        for (let c = 0; c < gridCols; c++) {
                            let sym = grid[r][c];
                            if (sym) {
                                sym.y += sym.vy;
                                sym.vy += 0.8; // drop acceleration
                                if (sym.y < canvas.height + 100) {
                                    activeClear = true;
                                }
                            }
                        }
                    }
                    if (!activeClear) {
                        // All cleared. Empty layout array
                        grid = Array(gridRows).fill(null).map(() => Array(gridCols).fill(null));
                        colossalJelly = null;
                        
                        // Proceed to spawning new falling block
                        initGrid();
                    }
                    break;

                case 'falling':
                    let allLanded = true;
                    const grav = turboMode ? 1.1 : 0.55;
                    const maxVy = turboMode ? 25 : 16;
                    
                    for (let c = 0; c < gridCols; c++) {
                        for (let r = 0; r < gridRows; r++) {
                            let sym = grid[r][c];
                            if (sym && sym.state === 'falling') {
                                allLanded = false;
                                sym.vy += grav;
                                if (sym.vy > maxVy) sym.vy = maxVy;
                                sym.y += sym.vy;
                                
                                if (sym.y >= sym.targetY) {
                                    sym.y = sym.targetY;
                                    sym.vy = 0;
                                    sym.state = 'resting';
                                    sym.bounceVel = -0.38; // squash land force
                                    playSound('impact');
                                }
                            }
                        }
                    }

                    // Run spring squash & stretch wobble on resting symbols
                    for (let r = 0; r < gridRows; r++) {
                        for (let c = 0; c < gridCols; c++) {
                            let sym = grid[r][c];
                            if (sym && sym.state === 'resting') {
                                updateSoftBodyWobble(sym);
                            }
                        }
                    }

                    if (allLanded) {
                        gameState = 'check_wins';
                    }
                    break;

                case 'check_wins':
                    // Detect matches
                    const matches = resolveGridClusters();
                    if (matches.length > 0) {
                        let totalSpinBonus = 0;
                        let maxClusterMult = 1;
                        
                        for (let cl of matches) {
                            let baseType = cl.type;
                            let cells = cl.cells;
                            let count = cells.length;
                            
                            // Multipliers inside cluster
                            let clusterMultiplier = 1;
                            let sumCoordsX = 0;
                            let sumCoordsY = 0;

                            for (let cell of cells) {
                                let sym = grid[cell.r][cell.c];
                                sumCoordsX += sym.x;
                                sumCoordsY += sym.y;
                                
                                if (sym.multiplier > 1) {
                                    clusterMultiplier += (sym.multiplier - 1); // add multipliers together
                                }
                                sym.isExploding = true;
                                sym.explodeScale = 1.0;
                            }

                            let clusterCenterX = sumCoordsX / count;
                            let clusterCenterY = sumCoordsY / count;

                            let clusterWin = 0;
                            
                            if (baseType === 'colossal') {
                                // Special progressive giant payout
                                let cObj = cl.colossalObj;
                                clusterWin = count * payouts['gold'] * cObj.multiplier * betAmount;
                                clusterMultiplier = cObj.multiplier;
                            } else {
                                // Standard payout calculation
                                let basePay = payouts[baseType] * betAmount;
                                clusterWin = count * basePay * clusterMultiplier;
                            }

                            totalSpinBonus += clusterWin;
                            
                            // Visuals
                            let colorMap = {
                                'cyan': '#00f3ff',
                                'magenta': '#ff007f',
                                'green': '#39ff14',
                                'purple': '#9d00ff',
                                'gold': '#ffd700',
                                'colossal': '#ffd700'
                            };
                            let colStr = colorMap[baseType];
                            
                            // Spawn explosions
                            for (let cell of cells) {
                                let sym = grid[cell.r][cell.c];
                                spawnClusterExplosion(sym.x, sym.y, colStr);
                            }

                            // Trigger floating numbers
                            floatingTexts.push({
                                x: clusterCenterX,
                                y: clusterCenterY,
                                text: `+$${clusterWin.toFixed(2)}${clusterMultiplier > 1 ? ` (${clusterMultiplier}x)` : ''}`,
                                color: colStr,
                                size: count > 8 ? 24 : 17,
                                vy: 1.5,
                                life: 0,
                                maxLife: 55
                            });

                            // Add to meter (2.0% per exploded symbol)
                            progressiveProgress = Math.min(100, progressiveProgress + count * 2.0);

                            // Sound: sweep pitch scales with size
                            playSound('pop', { pitch: 350 + (count * 40) });
                        }

                        spinWin += totalSpinBonus;
                        balance += totalSpinBonus;
                        updateUI();
                        
                        // Check Win Celebrations (BIG/MEGA/COLOSSAL)
                        let multScale = totalSpinBonus / betAmount;
                        if (multScale >= 50.0) {
                            winCelebration = { text: 'COLOSSAL WIN!', winAmt: totalSpinBonus, timer: 120, scale: 0 };
                            playSound('win_tune', { multiplier: 7 });
                        } else if (multScale >= 20.0) {
                            winCelebration = { text: 'MEGA WIN!', winAmt: totalSpinBonus, timer: 100, scale: 0 };
                            playSound('win_tune', { multiplier: 5 });
                        } else if (multScale >= 5.0) {
                            winCelebration = { text: 'BIG WIN!', winAmt: totalSpinBonus, timer: 80, scale: 0 };
                            playSound('win_tune', { multiplier: 2 });
                        } else {
                            playSound('win_tune', { multiplier: 1 });
                        }

                        shakeIntensity = Math.min(22, shakeIntensity + totalSpinBonus * 1.5);
                        timerDelay = turboMode ? 160 : 450;
                        gameState = 'exploding';
                    } else {
                        // Check for progressive bonus trigger when cascades cease
                        if (progressiveProgress >= 100) {
                            gameState = 'colossal_intro';
                            timerDelay = turboMode ? 350 : 1200;
                        } else {
                            // Finished spin
                            gameState = 'idle';
                            updateUI();
                            
                            // Auto Spin Trigger delay
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

                case 'exploding':
                    timerDelay -= dt;
                    for (let r = 0; r < gridRows; r++) {
                        for (let c = 0; c < gridCols; c++) {
                            let sym = grid[r][c];
                            if (sym && sym.isExploding) {
                                sym.explodeScale *= 0.82; // Shrink animation
                            } else if (sym) {
                                updateSoftBodyWobble(sym);
                            }
                        }
                    }
                    if (colossalJelly) updateSoftBodyWobble(colossalJelly);

                    if (timerDelay <= 0) {
                        // Remove exploded symbols from array
                        for (let r = 0; r < gridRows; r++) {
                            for (let c = 0; c < gridCols; c++) {
                                if (grid[r][c] && grid[r][c].isExploding) {
                                    grid[r][c] = null;
                                }
                            }
                        }
                        // Clear colossal reference if it was detonated
                        if (colossalJelly && colossalJelly.isExploding) {
                            colossalJelly = null;
                            progressiveProgress = 0; // reset charge
                            shadowOverlayAlpha = 0;
                        }
                        
                        gameState = 'cascading';
                    }
                    break;

                case 'cascading':
                    // 1. Shift cells down to replace empty cells
                    for (let c = 0; c < gridCols; c++) {
                        let emptyCount = 0;
                        for (let r = gridRows - 1; r >= 0; r--) {
                            if (grid[r][c] === null) {
                                emptyCount++;
                            } else if (emptyCount > 0) {
                                // Shift symbol down
                                let sym = grid[r][c];
                                grid[r][c] = null;
                                grid[r + emptyCount][c] = sym;
                                sym.gridY = r + emptyCount;
                                sym.targetY = gridStartY + sym.gridY * (cellWidth + gap) + cellWidth / 2;
                                sym.state = 'falling';
                            }
                        }
                        
                        // 2. Spawn replacement symbols staggered above grid
                        for (let i = 0; i < emptyCount; i++) {
                            let targetRow = emptyCount - 1 - i;
                            let spawnY = -(i + 1) * (cellWidth + gap) - 30;
                            grid[targetRow][c] = spawnSymbol(c, targetRow, spawnY);
                        }
                    }
                    
                    gameState = 'falling';
                    break;

                case 'colossal_intro':
                    // Ambient ocean turns dark vignette
                    shadowOverlayAlpha += (0.8 - shadowOverlayAlpha) * 0.08;
                    alertOverlay = { text: 'COLOSSAL JELLY INCOMING', alpha: 1.0, timer: 90 };
                    
                    timerDelay -= dt;
                    if (timerDelay <= 0) {
                        gameState = 'colossal_falling';
                        
                        // Pick Colossal size (2x2 to 5x5) based on probability weights
                        const rVal = Math.random();
                        let S = 3; // default 3x3
                        if (rVal < 0.45) S = 3;
                        else if (rVal < 0.85) S = 4;
                        else S = 5; // massive 5x5

                        // Fit Colossal boundary indices inside grid boundaries
                        const maxCol = gridCols - S;
                        const maxRow = gridRows - S;
                        const sc = Math.floor(Math.random() * (maxCol + 1));
                        const sr = Math.floor(Math.random() * (maxRow + 1));

                        // Spawn parameters
                        const targetX = gridStartX + sc * (cellWidth + gap) + (S * cellWidth + (S - 1) * gap) / 2;
                        const targetY = gridStartY + sr * (cellWidth + gap) + (S * cellWidth + (S - 1) * gap) / 2;

                        // Golden progressive multiplier range (x5 to x100)
                        const mults = [5, 10, 10, 15, 15, 20, 25, 50, 100];
                        const mult = mults[Math.floor(Math.random() * mults.length)];

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
                            multiplier: mult,
                            state: 'falling',
                            isColossal: true,
                            isExploding: false,
                            explodeScale: 1.0
                        };

                        playSound('spin');
                    }
                    break;

                case 'colossal_falling':
                    colossalReticleAlpha += (0.6 - colossalReticleAlpha) * 0.1;
                    
                    const cGrav = turboMode ? 1.6 : 0.85;
                    colossalJelly.vy += cGrav;
                    colossalJelly.y += colossalJelly.vy;
                    
                    if (colossalJelly.y >= colossalJelly.targetY) {
                        colossalJelly.y = colossalJelly.targetY;
                        colossalJelly.vy = 0;
                        colossalJelly.state = 'resting';
                        colossalJelly.bounceVel = -0.58; // heavy land impact squash
                        
                        gameState = 'colossal_impact';
                        timerDelay = turboMode ? 200 : 650;
                    }
                    break;

                case 'colossal_impact':
                    playSound('colossal_impact');
                    shakeIntensity = 26; // Heavy screenshake
                    colossalReticleAlpha = 0;

                    // Ring Shockwave FX
                    shockwaves.push({
                        x: colossalJelly.x,
                        y: colossalJelly.y,
                        radius: 20,
                        maxRadius: 400,
                        speed: turboMode ? 16 : 10,
                        alpha: 1.0,
                        width: 16
                    });

                    // Shatter and vaporize all standard symbols beneath colossal block boundaries
                    const sr = colossalJelly.gridY;
                    const sc = colossalJelly.gridX;
                    const S = colossalJelly.size;
                    
                    for (let r = sr; r < sr + S; r++) {
                        for (let c = sc; c < sc + S; c++) {
                            if (grid[r][c] && !grid[r][c].isColossal) {
                                // Spawn visual pops
                                spawnClusterExplosion(grid[r][c].x, grid[r][c].y, '#00f3ff');
                                grid[r][c] = null;
                            }
                            // Map grid cells to Colossal reference
                            grid[r][c] = colossalJelly;
                        }
                    }

                    gameState = 'colossal_pay';
                    break;

                case 'colossal_pay':
                    updateSoftBodyWobble(colossalJelly);
                    // Force land checking: check and execute pay calculation
                    gameState = 'check_wins'; 
                    break;

                case 'idle':
                    // Keep idle ambient sway animation running
                    for (let r = 0; r < gridRows; r++) {
                        for (let c = 0; c < gridCols; c++) {
                            let sym = grid[r][c];
                            if (sym) updateSoftBodyWobble(sym);
                        }
                    }
                    if (colossalJelly) updateSoftBodyWobble(colossalJelly);
                    shadowOverlayAlpha += (0 - shadowOverlayAlpha) * 0.05;
                    break;
            }
        }

        // Spring-Mass soft body wobble simulator
        function updateSoftBodyWobble(sym) {
            const stiffness = 0.16;
            const damping = 0.14;
            
            let force = -stiffness * (sym.scaleY - 1.0);
            let damp = -damping * sym.bounceVel;
            let acc = force + damp;
            
            sym.bounceVel += acc;
            sym.scaleY += sym.bounceVel;
            sym.scaleX = 2.0 - sym.scaleY; // Scale preservation formula

            // Soft body idle breathing/drift wobble when resting
            if (sym.state === 'resting' && Math.abs(sym.scaleY - 1.0) < 0.005 && Math.abs(sym.bounceVel) < 0.005) {
                // Return to pure idle wave breathing
                sym.scaleY = 1.0;
                sym.scaleX = 1.0;
                sym.bounceVel = 0;
            }
        }


        // --- RENDER TICK LOOP ---
        function render(time) {
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // 1. Context translation shake FX
            ctx.save();
            if (shakeIntensity > 0.1) {
                let dx = (Math.random() * 2 - 1) * shakeIntensity;
                let dy = (Math.random() * 2 - 1) * shakeIntensity;
                ctx.translate(dx, dy);
            }

            // 2. Bioluminescent ambient caustics (ocean light rays)
            ctx.save();
            ctx.globalCompositeOperation = 'screen';
            ctx.fillStyle = 'rgba(0, 243, 255, 0.03)';
            for (let i = 0; i < 4; i++) {
                let rayX = (canvas.width / 4) * i + Math.sin(time * 0.001 + i) * 30;
                let w1 = 40 + Math.sin(time * 0.002 + i) * 15;
                let w2 = 120 + Math.sin(time * 0.001 + i) * 40;
                
                ctx.beginPath();
                ctx.moveTo(rayX - w1, -10);
                ctx.lineTo(rayX + w1, -10);
                ctx.lineTo(rayX + w2 + 80, canvas.height + 10);
                ctx.lineTo(rayX - w2 - 80, canvas.height + 10);
                ctx.closePath();
                ctx.fill();
            }
            ctx.restore();

            // 3. Ambient floating background bubbles
            for (let b of bubbles) {
                ctx.save();
                ctx.globalAlpha = b.opacity;
                ctx.strokeStyle = '#ffffff';
                ctx.lineWidth = 1;
                ctx.beginPath();
                ctx.arc(b.x, b.y, b.r, 0, Math.PI * 2);
                ctx.stroke();
                
                // Highlight glint
                ctx.fillStyle = '#ffffff';
                ctx.beginPath();
                ctx.arc(b.x - b.r * 0.3, b.y - b.r * 0.3, b.r * 0.2, 0, Math.PI * 2);
                ctx.fill();
                ctx.restore();
            }

            // 4. Draw slot cells background grid borders
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

            // 5. Ambient deep ocean shadow overlay for colossal activation
            if (shadowOverlayAlpha > 0.01) {
                ctx.save();
                ctx.fillStyle = `rgba(3, 8, 14, ${shadowOverlayAlpha})`;
                ctx.fillRect(gridStartX - 5, gridStartY - 5, gridCols * (cellWidth + gap) - gap + 10, gridRows * (cellWidth + gap) - gap + 10);
                ctx.restore();
            }

            // 6. Colossal target grid landing indicator/reticle
            if (colossalJelly && colossalJelly.state === 'falling' && colossalReticleAlpha > 0.01) {
                ctx.save();
                ctx.globalAlpha = colossalReticleAlpha * (0.8 + Math.sin(time * 0.01) * 0.2);
                ctx.strokeStyle = '#ffd700';
                ctx.lineWidth = 3;
                ctx.shadowBlur = 20;
                ctx.shadowColor = '#ffd700';
                
                const S = colossalJelly.size;
                const rx = gridStartX + colossalJelly.gridX * (cellWidth + gap);
                const ry = gridStartY + colossalJelly.gridY * (cellWidth + gap);
                const rSize = S * cellWidth + (S - 1) * gap;
                
                ctx.strokeRect(rx, ry, rSize, rSize);
                
                // Crosshairs
                ctx.beginPath();
                ctx.moveTo(rx + rSize/2, ry - 15);
                ctx.lineTo(rx + rSize/2, ry + rSize + 15);
                ctx.moveTo(rx - 15, ry + rSize/2);
                ctx.lineTo(rx + rSize + 15, ry + rSize/2);
                ctx.stroke();
                
                ctx.restore();
            }

            // 7. Draw symbols
            let wavePhase = time * 0.04;
            
            // Draw normal symbols
            for (let r = 0; r < gridRows; r++) {
                for (let c = 0; c < gridCols; c++) {
                    let sym = grid[r][c];
                    // Skip drawing colossal index placeholders
                    if (sym && !sym.isColossal) {
                        let scale = sym.isExploding ? sym.explodeScale : 1.0;
                        drawJellyfishSymbol(
                            ctx,
                            sym.type,
                            sym.x,
                            sym.y,
                            20, // size radius
                            wavePhase + (c * 0.4) + (r * 0.3),
                            sym.scaleX * scale,
                            sym.scaleY * scale,
                            sym.multiplier
                        );
                    }
                }
            }

            // Draw Colossal Jellyfish on top of normal symbols
            if (colossalJelly) {
                let scale = colossalJelly.isExploding ? colossalJelly.explodeScale : 1.0;
                drawColossalJellyfish(
                    ctx,
                    colossalJelly.x,
                    colossalJelly.y,
                    colossalJelly.size * 25, // proportional radius size
                    wavePhase * 0.8,
                    colossalJelly.scaleX * scale,
                    colossalJelly.scaleY * scale,
                    colossalJelly.multiplier
                );
            }

            // 8. Render Shockwaves & Particle explosions
            updateAndDrawShockwaves();
            updateAndDrawParticles();
            updateAndDrawFloatingTexts();

            // 9. Screenshake context restore
            ctx.restore();

            // 10. Progressive Bar HUD drawn directly on Canvas top
            drawProgressiveHUD(time);

            // 11. Large Win Celebrations Banner Overlay
            drawWinCelebrationOverlay(time);
            
            // 12. Spark alerts
            drawAlertOverlay(time);
        }

        // Draw HUD progressive meter
        function drawProgressiveHUD(time) {
            const barX = gridStartX;
            const barY = 32;
            const barW = gridCols * (cellWidth + gap) - gap;
            const barH = 14;
            
            ctx.save();
            // Background slot tube
            ctx.fillStyle = '#0a131b';
            ctx.strokeStyle = 'rgba(255, 255, 255, 0.05)';
            ctx.lineWidth = 1;
            ctx.beginPath();
            ctx.roundRect(barX, barY, barW, barH, 7);
            ctx.fill();
            ctx.stroke();

            // Charged fill
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
            
            // Title Label overlay
            ctx.fillStyle = '#8a9db0';
            ctx.shadowBlur = 0;
            ctx.font = '800 10px "Outfit", sans-serif';
            ctx.textAlign = 'left';
            ctx.textBaseline = 'middle';
            ctx.fillText('PROGRESSIVE JELLY CHARGE', barX + 8, barY + barH/2);
            
            ctx.textAlign = 'right';
            ctx.fillStyle = currentProgress >= 100 ? '#ffd700' : '#ffffff';
            ctx.font = '800 11px "Outfit", sans-serif';
            ctx.fillText(currentProgress >= 100 ? 'READY!' : `${Math.floor(currentProgress)}%`, barX + barW - 8, barY + barH/2);
            ctx.restore();
        }

        function drawWinCelebrationOverlay(time) {
            if (winCelebration.timer <= 0) return;
            winCelebration.timer--;
            
            // Pulse & scale intro math
            if (winCelebration.timer > 100) {
                winCelebration.scale += (1.0 - winCelebration.scale) * 0.15;
            } else if (winCelebration.timer < 20) {
                winCelebration.scale += (0.0 - winCelebration.scale) * 0.15;
            }

            ctx.save();
            ctx.globalAlpha = Math.min(1.0, winCelebration.timer / 15);
            
            // Spotlight backdrop
            let spotlight = ctx.createRadialGradient(canvas.width/2, canvas.height/2, 20, canvas.width/2, canvas.height/2, 280);
            spotlight.addColorStop(0, 'rgba(15, 33, 46, 0.85)');
            spotlight.addColorStop(1, 'rgba(15, 33, 46, 0.0)');
            ctx.fillStyle = spotlight;
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            // Scale text container
            ctx.translate(canvas.width/2, canvas.height/2 - 20);
            ctx.scale(winCelebration.scale, winCelebration.scale);

            // Neon glowing header
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            ctx.font = '800 38px "Outfit", sans-serif';
            
            // Alternating glow colors based on win size
            let colors = ['#ffd700', '#ff007f', '#00f3ff'];
            let chosenColor = colors[Math.floor(time / 200) % colors.length];
            
            ctx.shadowBlur = 25;
            ctx.shadowColor = chosenColor;
            ctx.fillStyle = '#ffffff';
            ctx.fillText(winCelebration.text, 0, -25);
            
            // Win Amount display
            ctx.fillStyle = '#00e701';
            ctx.shadowColor = '#00e701';
            ctx.font = '800 46px "Outfit", sans-serif';
            ctx.fillText(`+$${winCelebration.winAmt.toFixed(2)}`, 0, 30);
            
            ctx.restore();
        }

        function drawAlertOverlay(time) {
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
            
            // Top/bottom neon borders
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

            // Text
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            ctx.font = '800 22px "Outfit", sans-serif';
            ctx.fillStyle = '#ffffff';
            ctx.fillText(alertOverlay.text, canvas.width/2, canvas.height/2);
            
            ctx.restore();
        }

        // --- MAIN ANIMATION TIMER LOOP ---
        function tick(time) {
            update(time);
            render(time);
            requestAnimationFrame(tick);
        }
        
        // Start animation frame loop
        requestAnimationFrame(tick);

    </script>
</body>
</html>
"""

# Render the game inside the Streamlit HTML component frame
components.html(html_code, height=920, scrolling=False)
