#!/usr/bin/env python3
"""Regenerate the 19 agent lines with ElevenLabs.

Usage:
  1. Put your key in the environment (never commit it):
       export ELEVENLABS_API_KEY=xi-...
     or write it to ~/.elevenlabs_key (single line).
  2. python3 gen_voice_11labs.py [voice_id]

Default voice: Adam (pNInz6obpgDQGcFmaJgB) — deep, steady, desk-appropriate.
Alternatives: Daniel 'onwK4e9ZLuTAKqWW03F9' (British news), Brian 'nPczCjzI2devNBz1zQrb'.
~2,300 chars total, fits the free tier (10k/month).
"""
import json, os, pathlib, sys, urllib.request

LINES = {
 'desk-boot': 'Desk is live. Positions and limits are loaded — give me an order.',
 'cold-boot': 'What do you want to own? Just say it — no account, no forms, no keyboard.',
 'wallet-offer': 'You don’t have a wallet yet — let’s make one. No seed phrase; your face is the key. Tap to create it.',
 'wallet-live': 'Wallet is live and passkey secured — it works across Bitcoin, Ethereum, Base and Arbitrum at once. Spending limits are set. How much do you want to put in?',
 'ask-amount': 'How much do you want to put in?',
 'quote': 'Best price locked — routed across every venue, and you keep more than any single venue would give you. It’s inside your limits. Say confirm.',
 'desk-order': 'Order parsed. Best fill is a split route across three venues — that keeps real money over the best single venue. It’s above your solo limit, so it needs a second approver. Say confirm.',
 'yield-scan': 'Scan done. Your stables are earning under their potential — there’s a stronger home on your approved list, same risk tier, no lock-up. The best route costs a fraction of the alternatives. Say confirm to move it.',
 'vault-offer': 'That cash can earn. Best risk-adjusted vault on your approved list — deposit from any chain, unwind anytime. Say confirm.',
 'policy': 'Twenty five thousand per trade, a hundred thousand a day, venue whitelist, and anything bigger needs a second approver. Kill switch armed.',
 'positions': 'Here’s everything you hold — every position in one view.',
 'no-pending': 'Nothing pending.',
 'cancelled': 'Cancelled. Nothing moved.',
 'nothing-yet': 'Nothing pending yet.',
 'buy-done': 'Done. It’s yours — held in your own wallet, not on an exchange. That took about thirty seconds, and you never touched a keyboard.',
 'desk-done': 'Filled. Settled on Base — split across three venues, dual approved, one signature. Receipt is signed.',
 'rebalance-done': 'Moved. Your yield just stepped up — and the route itself kept real money over the next best. Receipt is signed.',
 'vault-done': 'Deposited. It’s earning now — say the word and I’ll unwind it anytime.',
 'fallback': 'Tell me what you want to own. For example, buy some bitcoin.',
}

def key():
    k = os.environ.get('ELEVENLABS_API_KEY')
    if not k:
        p = pathlib.Path.home() / '.elevenlabs_key'
        if p.exists(): k = p.read_text().strip()
    if not k:
        sys.exit('No key. export ELEVENLABS_API_KEY=... or write ~/.elevenlabs_key')
    return k

VOICE = sys.argv[1] if len(sys.argv) > 1 else 'pNInz6obpgDQGcFmaJgB'  # Adam
OUT = pathlib.Path(__file__).parent / 'voice'
K = key()

for name, text in LINES.items():
    req = urllib.request.Request(
        f'https://api.elevenlabs.io/v1/text-to-speech/{VOICE}?output_format=mp3_44100_128',
        data=json.dumps({
            'text': text,
            'model_id': 'eleven_multilingual_v2',
            'voice_settings': {'stability': 0.55, 'similarity_boost': 0.8, 'style': 0.25},
        }).encode(),
        headers={'xi-api-key': K, 'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=60) as r:
        (OUT / f'{name}.mp3').write_bytes(r.read())
    print('ok', name)
print('done — refresh the demo page')
