# irc-music-generation

Lame title, but that's basically what this is: a bot that reads 
chat in an IRC channel and converts it into music. Basically, 
it's like windchimes, but not.

This project would not have been possible without [FoxDot](http://foxdot.org/), which 
is a cool livecoding music project. Check it out.

## Details of the Proof of Concept

As of 4/23/2018, the code does the following.

1. Connects to an IRC (twitch) channel.
2. Reads the text that people type.
3. Turns what people type into music.

The way the bot turns text into music is through a fairly simple set of 
rules. It's a hair arbitrary, but not so arbitrary as to be complete 
cheating. At least, such is the case for this first iteration.

1. Percussion is generated based on consonants. Case matters.
2. Chords are determined by part of speech. Part of speech tagging 
is done through the NLTK library.
3. The bass line is generated through Part of speech tagging as well.
4. The meter is derived from the average length of words. If the average 
length is odd, the meter is 3/4. If it's even, then 4/4.

The scales used change every 15 seconds or so (depending on the next time 
someone posts something in chat), which affects the notes played by the 
chords and the bass.

### Why doesn't this sound as awful as I thought it would?

I cheated. The harmonies used are all a mix of major and minor that have 
somewhere between one and three flats, so it's never too jarring. For 
example, one key is d minor (technically: it's aeolian because the raised
seventh is never used--just d natural minor all the way through).

## Configuration

This isn't elaborate enough that I can imagine anyone wanting to clone it, 
especially because of how ugly the code is at the moment (I know that I should 
clean as I go, but I really wanted to just hack something together quickly to 
see if I could get it working). On the off chance you do, you'll need to set up 
FoxDot, you'll need NLTK, and you'll need the IRC package.

You'll need to modify the bot.py file to have it point towards whichever channel 
you want to have the bot read from. If you're doing it with twitch, you'll need to 
use your own oauth. Furthermore, you'll need to adjust the parameters in the IRCer
if there is no oauth.

---

## Wishlist

With any project, there's always more you can do. This one is no 
different. In the section that follows, I'm providing a list of 
some of the features that I immediately want to incorporate, and 
things that I might want to do later.

(to be added later)