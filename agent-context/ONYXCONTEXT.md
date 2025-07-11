ONYX Integration Guide – OSC, DMX, and NDI in Obsidian Control Systems
Obsidian Control Systems’ ONYX is a powerful lighting control software platform designed for both hardware consoles and PC. This guide provides a deep dive into integrating ONYX with external systems using Open Sound Control (OSC), DMX (Digital Multiplex) output, and NDI (Network Device Interface) streaming. We’ll cover how to enable these interfaces, the address structures and mappings (with focus on main playback faders and buttons), and strategies for combining OSC, DMX, and NDI to link ONYX with media servers (e.g. Resolume Arena) or interactive tools (e.g. TouchDesigner).
OSC Integration in ONYX
Open Sound Control (OSC) allows remote control of ONYX playbacks, faders, buttons and more via network messages. ONYX’s OSC support lets external devices (like tablets running TouchOSC or custom controllers) both control ONYX and receive feedback from it
support.obsidiancontrol.com
support.obsidiancontrol.com
. Below we detail how to enable OSC, the OSC address patterns for ONYX controls, and example use cases for triggering cues remotely.
Enabling and Configuring OSC in ONYX
To use OSC, first ensure ONYX’s OSC interface is enabled and configured correctly:
Network Settings: Open ONYX’s menu (MENU button or the ONYX logo) and navigate to Main Menu > Network > Settings > Interfaces. Ensure the network adapter (typically labeled “REMOTE”) is active with a valid IP (use Automatic/DHCP or a static IP suitable for your network). Enable OSC on the Remote adapter and press Apply
support.obsidiancontrol.com
support.obsidiancontrol.com
.
OSC Setup: Next, go to Main Menu > OSC. Under Settings, turn on OSC for the Remote interface. In the Devices section, activate an OSC Device slot (ONYX supports multiple OSC devices)
support.obsidiancontrol.com
support.obsidiancontrol.com
. Give the device a name (e.g. “Tablet Remote”) and set the Address to the IP address of your OSC controller (for example, the IP of your tablet running TouchOSC). Configure the Port numbers: ONYX’s “Output Port” should match the listening port of your controller, and the “Input Port” should match the port your controller sends to
support.obsidiancontrol.com
support.obsidiancontrol.com
. Press Update and then Apply to confirm changes.
Establish Connection: Finally, on the external OSC device, use the same network and port settings. For TouchOSC, enter ONYX’s IP and the ports, then refresh or sync the layout. If ONYX is not in a restricted mode (see note on licensing below), the connection will establish and ONYX will begin sending/receiving OSC messages. You should see fader movements or button presses reflected on the remote, and vice versa
support.obsidiancontrol.com
support.obsidiancontrol.com
.
Note: In ONYX Free/Nova mode (PC running without certain hardware licenses), OSC functionality is locked or time-limited to trial mode
support.obsidiancontrol.com
support.obsidiancontrol.com
. For full OSC I/O, ensure you have the appropriate license or hardware (e.g. connecting an NX Touch hardware controller enables OSC in “NOVA+” mode
support.obsidiancontrol.com
support.obsidiancontrol.com
).

https://support.obsidiancontrol.com/Content/Onyx_Manual/Networking/OSC.htm
Screenshot: ONYX’s OSC configuration – enabling an OSC remote device with IP and port. ONYX allows multiple OSC devices (each with its own “Device Space” and settings) to control different banks or consoles.
OSC Address Pattern Structure (Main Faders & Buttons)
All OSC addresses in ONYX start with the prefix /Mx
forum.obsidiancontrol.com
. Under this prefix, ONYX organizes controls into several categories of addresses:
Faders: /Mx/fader/<faderId> – Controls the level of a playback fader. The faderId is a numeric identifier mapped to a physical fader. For the 10 main playback faders (Device Space 0, Page 1 by default), the IDs range from 4203 up to 4293 (in steps of 10)
forum.obsidiancontrol.com
. For example, /Mx/fader/4203 corresponds to the first playback fader, /Mx/fader/4213 to the second, and so on up to /Mx/fader/4293 for the tenth fader. Each fader expects an integer value 0–255 (0 = 0%, 255 = 100% level) for both setting the fader and as feedback
forum.obsidiancontrol.com
forum.obsidiancontrol.com
. (Since ONYX 4.8, additional faders 11–20 became accessible as 4603–4693 for consoles that have them
forum.obsidiancontrol.com
.)
Buttons: /Mx/button/<buttonId> – Triggers a button press (such as a playback button or flash key). The buttonId is a numeric code for a specific button. ONYX distinguishes LCD buttons (labeled buttons with text) and LED buttons (those with indicator LEDs) but both use /Mx/button/ addresses
forum.obsidiancontrol.com
forum.obsidiancontrol.com
. A button press is sent as value 1 for “down” (pressed) and 0 for “up” (released)
forum.obsidiancontrol.com
. Many console buttons also have feedback sub-addresses: e.g. /Mx/button/<id>/led provides LED state (0=off, 1=on)
forum.obsidiancontrol.com
 and /Mx/button/<id>/text provides the button label text string
forum.obsidiancontrol.com
. The specific buttonId numbers correspond to console front-panel controls (for example, main playback Go/Flash buttons above/below faders have unique IDs). In practice, you can use the predefined TouchOSC layouts or ONYX’s OSC reference PDF to find the exact IDs for each button.
Playback Actions: /Mx/playback/page<X>/<Y>/<action> – High-level cue playback triggers that don’t require knowing the raw IDs. This is especially useful for triggering cues remotely. The <X> is the playback Page number and <Y> is the Playback fader number on that page. The <action> can be go, pause, release, select (to “GO” the cue, pause it, release it, or select that cuelist)
forum.obsidiancontrol.com
. For example, to press the GO button on Page 1, Fader 3, send an OSC message to /Mx/playback/page1/3/go. To pause the cue on Page 5, Fader 20: /Mx/playback/page5/20/pause
forum.obsidiancontrol.com
. (Note: ONYX will execute these incoming commands, but as of the documented version, it does not send playback status feedback via OSC yet for cuelist state changes
forum.obsidiancontrol.com
.)
Other Controls: Additional categories include Programmer knobs and wheels (/Mx/encoder/…, /Mx/scroll/…), parameter belts (/Mx/belt/…), Grand Master and special keys, etc. For example, the Grand Master fader can be controlled via a dedicated address (there is a specific OSC control for Grand Master in ONYX’s mapping, though it may also appear as a fader with its own ID)
showcockpit.com
. Scroll wheels use paths like /Mx/scroll/<wheelId>/<direction> (e.g. /Mx/scroll/4110/up with value 1 to scroll up)
forum.obsidiancontrol.com
. Most of these are advanced controls, whereas this guide emphasizes the main playbacks.
Device Spaces and Pages: ONYX uses the concept of Device Space for OSC to allow multiple sets of playbacks to be controlled independently. DeviceSpace 0 corresponds to the main playback bank shown on the console UI (the first 10 faders on the current page)
showcockpit.com
. If you need to control multiple pages or an extended wing of playbacks simultaneously via OSC, ONYX lets you configure additional OSC devices with different DeviceSpace numbers – each can target a different page/bank of faders
forum.obsidiancontrol.com
. In practice, one OSC “device” could be fixed to Page 1 (deviceSpace 0), another to Page 2 (deviceSpace 1), etc., allowing an external controller to access, say, faders 1–10 on multiple pages at once. This requires setting the Wing ID or device space in the OSC device properties (as shown in the OSC setup screenshot above). Feedback: ONYX sends OSC feedback for certain elements: main playback fader levels, button LED states, text labels, etc., will be transmitted to the OSC device (to keep a remote interface in sync)
forum.obsidiancontrol.com
forum.obsidiancontrol.com
. For example, when a cue’s name changes, ONYX might send /Mx/button/<id>/text "New Name" to update a remote display label. Important: ONYX only provides feedback for the standard mapped controls (Main playback faders/buttons, programmer keys, F-keys, etc.). If you repurpose a fader or button to a custom function that’s not in OSC’s supported list, it won’t send feedback for that control
showcockpit.com
. Best practice is to use the main playbacks and known OSC-addressable keys if two-way sync is required.
Example: Controlling ONYX via OSC
Using the above addresses, external software or devices can remotely trigger ONYX cues or faders. Below are a few practical examples:
Fader Level Control: To remotely fade a light intensity submaster on playback fader 1, send an OSC message with address /Mx/fader/4203 and an integer value. For instance, /Mx/fader/4203 128 would set fader 1 to roughly 50% (128 out of 255). ONYX will also output fader movements on this address if the fader is moved locally
forum.obsidiancontrol.com
, allowing bi-directional sync (the external controller’s fader knob will move when ONYX’s fader moves).
Cue GO Trigger: To trigger the GO button of a cuelist on the 3rd fader of the current page, send an OSC command to /Mx/playback/page1/3/go. This is equivalent to pressing the “GO” button for that playback, firing the next cue in that cuelist
forum.obsidiancontrol.com
. Likewise, /Mx/playback/page1/3/release would release that cuelist (stop output) remotely.
Button Press (Flash or Bump): If you have a “flash” button on fader 5 (for example, a bump that brings lights to full while held), determine its OSC button ID (from documentation or layout). It might be an LED button with ID say 4251 (hypothetically). You would send /Mx/button/4251 1 to press it down (flash on) and /Mx/button/4251 0 to release it (flash off). ONYX will also send /Mx/button/4251/led 1 or 0 to your OSC client indicating the LED state if that button has an LED indicator.
Selecting Fixtures or Programmer Keys: ONYX’s OSC also covers some programmer commands. For example, /Mx/button/6101 1 might correspond to pressing the Group 1 button (if 6101 is the ID for a screen button). Similarly, there are OSC addresses for keys like Record, Clear, etc., using the /Mx/button/<id> scheme (the ShowCockpit documentation lists many under “Key” with names, but via OSC they are numeric IDs)
showcockpit.com
. This allows an OSC controller to operate ONYX’s command line (e.g., pressing the Full or Clear keys via OSC).
Use Cases: OSC control is commonly used for integrating ONYX with interactive applications or remote UIs:
A TouchOSC layout on a tablet can mimic the console’s faders and playback buttons, allowing a lighting operator to walk the venue and still control intensity or trigger cues from the tablet. ONYX provides official TouchOSC layout files for iPhone/iPad that correspond to these OSC addresses
support.obsidiancontrol.com
support.obsidiancontrol.com
.
A show control system or timeline software (e.g. QLab, Ableton, or a custom app) could send OSC cues to ONYX. For instance, a media timeline might send /Mx/playback/page1/1/go at specific timecodes to synchronize lighting cues with video or audio playback.
An interactive installation using TouchDesigner or Max/MSP could adjust lighting in real-time by sending OSC based on sensor input. For example, if a user’s movement is detected, TouchDesigner could send an OSC message to raise fader 2, bringing up a lighting look.
Conversely, ONYX’s OSC feedback can be utilized to monitor the lighting state externally. A custom application could listen to OSC from ONYX to know when a particular cue has executed or a fader level changed, and then trigger other actions (like starting a video or logging events).
Best Practices for OSC with ONYX
Match Ports and IPs: The OSC “Input” port in ONYX is where it listens (others should send to this port), and the “Output” port is where it transmits feedback (others should listen on this). Ensure these are not conflated. For example, if ONYX’s OSC device is set to Address 192.168.0.50 port 8000, and your controller is at 192.168.0.51, the controller should send to 192.168.0.50:8000, and you’d set the controller’s listening port (for feedback) to, say, 9000 while ONYX’s Output Port is 9000, Address 192.168.0.51
support.obsidiancontrol.com
support.obsidiancontrol.com
.
Use Device Spaces for multiple banks: If you need to access more than 10 playbacks via OSC simultaneously, configure additional OSC devices in ONYX with incremented DeviceSpace (each additional OSC device will appear as a new set of 10 faders). For instance, an OSC controller with 20 fader knobs can be split into two OSC devices in ONYX: one controlling playbacks 1–10 on the current page, and another set to DeviceSpace 1 controlling playbacks 11–20 (or page 2 faders 1–10, depending on console configuration). Note that originally ONYX did not support OSC for faders 11–20, but as of ONYX 4.8 these were added with the 4600-series IDs
forum.obsidiancontrol.com
.
Stick to supported controls: Remember that not every console function is exposed via OSC. Main playbacks and common keys are accessible, but some advanced or UI-only features might not have an OSC hook. Always refer to the official OSC mapping document (the “OSC MAPPING v1.20” PDF
forum.obsidiancontrol.com
) for the full list of addresses. If a function isn’t listed, you might need to use an alternate integration method (e.g., using MIDI or DMX Input as a trigger instead).
Latency and Network: OSC runs over UDP (in ONYX’s implementation), which is fast but not guaranteed delivery. Ensure your network is reliable (wired Ethernet for critical show control is recommended over WiFi). Keep the OSC message rate reasonable; ONYX will send continuous fader feedback as values change which can be high frequency if multiple faders move – a robust network and avoiding WiFi congestion helps maintain responsiveness.
Now that we’ve covered OSC, let’s examine DMX output – how ONYX outputs to lighting networks and how those DMX signals can be leveraged in an integration context.
DMX Output Configuration in ONYX
ONYX is fundamentally a DMX lighting controller supporting a large number of universes and various output protocols. Understanding how ONYX maps DMX universes and how playback actions translate to DMX output is key for integrating it with other systems (for example, sending DMX data to media servers or capturing DMX for visualization). This section covers ONYX’s DMX universe management, the effect of playbacks on DMX values, and methods to use DMX as an integration endpoint.
DMX Universes and Mapping in ONYX
A DMX universe consists of 512 channels, and ONYX supports up to 128 universes of output from a single system
d295jznhem2tn9.cloudfront.net
. In practical terms, that’s up to 65,536 DMX channels – suitable for very large lighting rigs. By default, the PC software in Free mode unlocks at least Universe 1 for output, and with entry-level hardware like an NX-DMX or NETRON node, up to 4 universes are freely available (NOVA mode)
support.obsidiancontrol.com
support.obsidiancontrol.com
. Higher licenses or console hardware (e.g. NX Wing, NX2, or USB license keys) unlock 64 or all 128 universes for use
support.obsidiancontrol.com
support.obsidiancontrol.com
. All 128 universes can be patched and programmed even in free mode, but without a license they won’t output data beyond the allowed count
support.obsidiancontrol.com
. Universe Configuration: ONYX allows output over both physical DMX ports (on consoles or USB-DMX devices) and network DMX protocols:
Physical Ports: If you’re using ONYX consoles or expansion hardware (NX Wing, NX DMX, etc.), the Local DMX menu is used to assign which universe is output on each physical XLR port. For example, an NX2 console has 4 DMX output ports – you could assign them to Universes 1–4 (or any arbitrary mapping) via the Local DMX settings
support.obsidiancontrol.com
support.obsidiancontrol.com
. Each port can also be toggled to act as an input if needed (for DMX In merging/control, discussed later)
support.obsidiancontrol.com
.
Network DMX (EtherDMX): ONYX supports Art-Net (ArtNet) and sACN (E1.31) for DMX-over-Ethernet. By default, all network DMX output is disabled until you enable it in settings
support.obsidiancontrol.com
. In the EtherDMX Settings (Main Menu > Network > EtherDMX), you can globally enable Art-Net and/or sACN output and specify the range of universes to send out
support.obsidiancontrol.com
support.obsidiancontrol.com
. ONYX will then broadcast or unicast those universes on the selected network interface. Art-Net can be set to broadcast (sending to all nodes) or unicast (only to detected nodes or specified IPs)
support.obsidiancontrol.com
support.obsidiancontrol.com
. sACN can be configured with priorities and as input/output as well
support.obsidiancontrol.com
. Typically, if integrating with media servers or other controllers, you would enable Art-Net/sACN output on the appropriate NIC (e.g., your show network) and ensure the other system is listening on the same protocol and universe numbers.
Universe Numbering: ONYX uses an intuitive 1-based numbering for universes in the UI (Universe 1, 2, 3, … up to 128). When outputting to Art-Net, those map to Art-Net universe IDs (be mindful that some software label Art-Net universes starting at 0; ONYX’s Universe 1 is Art-Net 0:0 by default, unless offset configured). For sACN, ONYX Universe 1 is sACN universe 1, etc., straightforwardly. In EtherDMX settings you can choose which range to output – e.g., output 1–4 if you only use four universes to reduce network load
support.obsidiancontrol.com
.
Patching Fixtures: Managing DMX output begins with patching fixtures to addresses. In ONYX’s Patch view, you assign each fixture to a universe and DMX address. ONYX keeps an internal table of the current value of each DMX channel (1–512 for each universe). When a fixture’s parameters change (through cues, manual programmer, etc.), ONYX updates those channel values and sends them out to any physical or network outputs mapped to that universe.
You can think of ONYX as maintaining a large 128 x 512 array of DMX values in real time. If Universe 5 is not enabled for output, changes in it won’t leave the console, but if later enabled or mapped to hardware, the latest values would start outputting.
ONYX supports flexible patching – you can patch multiple fixtures overlapping on the same channel (though typically not recommended unless intentionally merging via HTP/LTP logic), and it supports merging DMX input (see below) which can override or combine with its own output.
Output Behavior with Playbacks: ONYX’s cue playback engine determines how values change on that DMX matrix:
Intensity Faders (HTP): By default, intensity parameters use HTP (Highest Takes Precedence) merging. If you raise a submaster fader that affects some dimmer channels, those channels’ output values will be the highest value from any active source (base cue vs submaster). Lowering a fader will reduce the output if that fader was the highest contributor. ONYX handles this automatically in the background; as an integrator you simply see that DMX channel values go up or down following the fader movement.
LTP Parameters: Attributes like color, gobo, position are usually Latest Takes Precedence (LTP). Triggering a cue will cause those channel values to snap or fade to the new value, and remain until another cue overrides them. A paused cuelist will hold its last output until released.
Playback Priorities and Overrides: ONYX offers override playbacks (e.g., flash buttons that momentarily override a value). For instance, a Flash button might send a fixture to 100% intensity while held, then release back to the previous value. In DMX output, you would see channel go to 255, then back down to whatever the cue had. ONYX 4.10 introduced Output overrides like Park, Highlight, etc., which also affect DMX out but those are more console operations (Park freezes a channel at a value, etc.)
usitt.org
.
Example – Fader affecting DMX: Suppose fader 1 is a master for House Lights (dimmer channels on Universe 1). When you move fader 1 up to 75%, ONYX scales the DMX values of all channels under that fader’s control to 75% of their programmed value. If house lights were at full (255) in the cue, they’ll output around 191 (75%) when the fader is at that level. ONYX sends these updated values out in the DMX stream live as you move the fader. If you watch an Art-Net/sACN monitor on Universe 1, you’ll see those channel values updating in real time. Output Latency & Rate: ONYX outputs DMX continuously, typically at around 40 frames per second per universe (this can be adjusted in some consoles). When multiple changes occur (multiple faders moved, chases running), ONYX will incorporate those changes into the next DMX frame. The system is designed to handle full 128 universes internally
d295jznhem2tn9.cloudfront.net
, but network and processing limits mean you should ensure your PC is robust (the ONYX manual recommends at least a Core i7 for full 128 universe usage)
support.obsidiancontrol.com
 if you ever scale that high. For most integrations (a few universes), performance is not an issue, but it’s good to note if using ONYX to drive large LED pixel maps into another system.
Exposing DMX to External Systems (Endpoints & Integration)
One strength of ONYX is that its DMX output can interface with many other show technology systems, since DMX (especially via Art-Net or sACN) is widely supported. Here are ways to leverage DMX in integrations:
Art-Net/sACN to Media Servers: Many media server software and VJ applications (Resolume, ArKaos, MadMapper, etc.) can be controlled via DMX. You can map DMX channels to trigger video clips, adjust effects or crossfade video layers. By configuring ONYX to output a dedicated universe for media control, you essentially treat the media server as a “fixture.” For example, Resolume Arena can listen to Art-Net: you could have ONYX Universe 50 mapped to Resolume’s parameters (Resolume lets you map DMX values to specific functions). In ONYX, you might patch a generic 512-channel “fixture” or use the CITP mapping (if available) for that media server. Then your lighting cues can also trigger video by sending DMX values. This is a unidirectional control (ONYX -> media server), using DMX as the messaging protocol.
ONYX to Lighting Visualizers: If you want to visualize or share what ONYX is doing with another system, you can send DMX to a visualizer or simulator. For instance, Capture, WYSIWYG, or LightConverse can receive Art-Net/sACN and render the lighting. Or a custom TouchDesigner patch could receive ONYX’s DMX to create generative art. Because ONYX supports industry-standard protocols, any external software that can receive those will work. Just ensure the network configuration in ONYX’s EtherDMX (IP and universe range) covers the target (for example, turn on sACN output for Universe 1-10 and in TouchDesigner use an sACN In CHOP listening to those universes).
Lighting Console Integration (Merging): In multi-console setups or take-over scenarios, ONYX can merge DMX input from another source. For example, you might have a primary console and ONYX as a backup or running in parallel. ONYX’s DMX Input feature allows treating incoming Art-Net/sACN or physical DMX as an input that can either merge with ONYX’s own output or control specific functions
support.obsidiancontrol.com
support.obsidiancontrol.com
. The DMX Input menu in ONYX provides three modes:
Merger: Direct DMX merging (HTP/LTP) where ONYX combines another console’s output with its own on a channel-by-channel basis
support.obsidiancontrol.com
.
Mapping: Map specific DMX channels from an external source to ONYX internal controls (e.g., channel 1 in could control a particular fixture’s intensity, or channel 5 could trigger a certain cuelist)
support.obsidiancontrol.com
support.obsidiancontrol.com
. For instance, you could use a small 24-channel DMX desk and map those faders to 24 selected fixtures’ intensities in ONYX
support.obsidiancontrol.com
. Or map a DMX channel to a cuelist’s fader so that external desk fader moves an ONYX playback fader.
Playback Control: A special mapping mode to control ONYX playback via DMX values. ONYX defines a channel scheme where incoming DMX on a “virtual playback remote” port can select page, playback number, cue number, and execute go/pause/release commands based on DMX ranges
support.obsidiancontrol.com
support.obsidiancontrol.com
. For example, by sending specific DMX values on channel 1–4 of a universe, you can remotely fire cues: Channel 1 sets the page, Channel 2 the fader, Channel 3 the cue number, Channel 4 the command (Go/Pause/Release) with predefined value ranges for each
support.obsidiancontrol.com
support.obsidiancontrol.com
. A DMX value of 10 on the “Command” channel might mean “Go”
support.obsidiancontrol.com
. This way, another lighting console or a timeline that can only send out DMX can still trigger specific cues in ONYX by crafting these values. It’s essentially OSC-like control but via DMX.
Bidirectional DMX Bridges: You could have ONYX and a media software influence each other via DMX. For instance, ONYX outputs Art-Net Universe 10 which a media server listens to (so lighting cues trigger video changes), and simultaneously the media server outputs Art-Net Universe 11 based on its state which ONYX takes in as DMX Input (maybe to fire backup cues or follow-along effects). While OSC or dedicated APIs are often cleaner for this, DMX is a robust fallback for compatibility.
Example – Resolume Clip Trigger via DMX: Let’s say we want ONYX’s playback button 1 (maybe a flash button) to trigger a video clip in Resolume. We could assign a DMX channel in Resolume’s DMX map to “Play clip 1”. If Resolume is listening to Art-Net Universe 100, Channel 5 for that trigger, we configure ONYX to output Universe 100 and patch a fixture whose channel 5 is controlled when we press that button (perhaps via a cuelist that sends value 255 on chan 5 momentarily). When the ONYX user presses that button, ONYX sends 255 on Universe 100:5, Resolume sees that and plays the clip. This shows how a lighting action can directly drive a video system through DMX. Reliability & Configuration Tips for DMX Integration:
Keep your network separated if possible: Art-Net/sACN vs NDI vs OSC – NDI (covered later) can flood a network with high bandwidth, so it’s common to run lighting protocols on one NIC or VLAN and NDI on another. ONYX’s EtherDMX settings allow you to select which network interface outputs Art-Net/sACN
support.obsidiancontrol.com
support.obsidiancontrol.com
. You might set a 2.x.x.x IP for Art-Net on one adapter and leave NDI on a 192.168.x.x adapter, for example.
Mind the universe counts: If you use a lot of pixel data via Dylos (which itself consumes DMX universes for LED pixels), ensure your license covers enough universes when integrating other systems. The ONYX Elite key unlocks all 128 universes
fullcompass.com
, which is useful if you plan to route many universes to external devices.
Always test the merge or mapping logic offline: If you plan to use DMX Input to have an external trigger ONYX, simulate it and watch ONYX’s logs or DMX Input monitor (ONYX provides a monitor to see incoming DMX on virtual ports
support.obsidiancontrol.com
). Off-by-one errors in universe numbers or channel values can confuse triggers (e.g., sending value 9 vs 10 might mean nothing happens if 10–19 is the “Go” range).
Next, we’ll explore ONYX’s support for NDI, which opens up video integration with the DYLOS pixel engine and how that can be applied in a show control system.
NDI Support in ONYX
In ONYX 4.10, support was added for NDI (Network Device Interface) streaming, which greatly enhances the ability to integrate with video content and media servers. NDI is a protocol for sending high-quality video (and audio) over a network with low latency. ONYX uses NDI primarily to input live video streams into the DYLOS pixel-mapping engine
theasc.com
usitt.org
, allowing dynamic video content to drive lighting across fixtures. We will outline ONYX’s NDI capabilities (input and any output), how to configure and use NDI streams in ONYX, and use cases such as feeding DYLOS generator output to other systems.
NDI Input: Receiving Live Video in DYLOS
Capabilities: ONYX can receive multiple NDI video streams from the network and treat them as media sources inside DYLOS. This means an external content source – e.g. Resolume Arena output, a camera feed, or a TouchDesigner generative graphic – can be sent as NDI, and ONYX will capture that stream and map it onto an array of fixtures (LED panels, pixel bars, etc.) via DYLOS. This effectively synchronizes lighting effects with video in real time. According to release notes, ONYX’s NDI support includes audio as well (for using audio waveforms/analysis in DYLOS), making it a comprehensive media input
theasc.com
forum.obsidiancontrol.com
. Enabling NDI in ONYX: To use NDI input, some one-time setup is required:
NDI Runtime: Ensure the NDI runtime/driver is installed. ONYX 4.10 comes with NDI support, and the NDI Settings page will show the NDI version installed
support.obsidiancontrol.com
.
NDI Network Interface: Go to Menu > NDI Settings in ONYX. Here, choose which network interface to use for NDI traffic (much like selecting an interface for Art-Net)
support.obsidiancontrol.com
. If you have multiple NICs, select the one on the same subnet as your NDI sources. Also enable “Local NDI Sources” if you plan to feed video from the same machine (for example, if Resolume is running on the same PC as ONYX, it can send to local NDI)
support.obsidiancontrol.com
.
NDI Nodes and Streams: ONYX will automatically discover NDI Nodes (devices or computers broadcasting NDI) on the network. In the NDI Settings > Nodes list, you should see the names of any NDI senders. You can toggle each node on or off; only Enabled nodes will be considered for input
support.obsidiancontrol.com
. Within each node, if it offers multiple streams (e.g., a machine could broadcast several different NDI feeds), ONYX lets you enable specific streams under the Input Streams section
support.obsidiancontrol.com
. Each stream can be toggled “Active” or “Ignored” individually
support.obsidiancontrol.com
. It’s good practice to disable any streams you don’t need, to save CPU/network load
support.obsidiancontrol.com
.
Quality and Bandwidth: ONYX’s NDI settings also provide options like Jitter Reduction (Low Latency vs Smooth Playback)
support.obsidiancontrol.com
. Low latency might be preferable for live camera feeds where timing is critical, whereas smooth playback might buffer a bit more for perfectly fluid video at the cost of a few frames delay. You’ll also see information about each stream such as resolution, frame rate, and whether it has an alpha channel
support.obsidiancontrol.com
. Ensure your network can handle the bandwidth of the NDI feeds (NDI can use dozens to hundreds of Mbps depending on resolution and frame rate).
Using NDI streams in DYLOS: Once NDI streams are enabled in settings, they become available as media sources in the DYLOS content library:
Open the Library window in ONYX (DYLOS Library, typically tab 5 in the DYLOS workspace). Switch to the Inputs tab
support.obsidiancontrol.com
. You’ll have a number of empty Input Slots (32 slots by default).
To create an NDI input source, right-click an empty slot (or hold EDIT and touch the slot) and choose “Create Input Source”
support.obsidiancontrol.com
. In the dialog, select Video under Processor, and then choose NDI Video as the source type
support.obsidiancontrol.com
. You should then get a list of available NDI streams (discovered from the enabled nodes). Select the desired NDI stream (for example, “Resolume Output 1”).
ONYX will create a Video Input Processor in that slot, linked to the chosen NDI feed
support.obsidiancontrol.com
. This item now behaves like a dynamic media file in DYLOS.
To use this NDI video on fixtures, go to a DYLOS Zone (open the DYLOS Composer view, typically view 4) and assign the input as content. Click on a Zone’s Source block and navigate to the Inputs tab to pick the Input slot you just configured
support.obsidiancontrol.com
support.obsidiancontrol.com
. Now the live video feed will be mapped across the pixels of that zone (which correspond to your lights).
You can treat the NDI feed just like any other video in DYLOS: apply effects, use palettes, scale/position it, etc. For example, if the NDI source is a live camera feed, you could have it drive an array of LED tiles or LED costumes in real-time. Audio via NDI: Not only video, NDI can carry audio which ONYX can use in its Audio Input, VU meter, spectrum features. As users on the forum discovered, ONYX can receive NDI-embedded audio and route it to Audio Analyzer processors (for beat synchronization or waveform effects)
forum.obsidiancontrol.com
forum.obsidiancontrol.com
. The workflow is: ensure the NDI stream’s audio is detected (NDI Settings will show channel count and sample rate for the stream
forum.obsidiancontrol.com
), then in the Library create an Audio input (or use the same Video Input but reference its audio) by selecting an Audio or VU Meter processor with NDI as the source
forum.obsidiancontrol.com
forum.obsidiancontrol.com
. ONYX can display a VU meter or waveform of the NDI audio and use it to modulate effects. This is great for music-driven light shows where the music is coming from a VJ software via NDI. (Note: Monitoring the actual audio output through ONYX requires setting up an audio output driver in ONYX’s I/O settings, as described in forum posts
forum.obsidiancontrol.com
forum.obsidiancontrol.com
.)
Using DYLOS Generator Patterns as NDI Content (Output)
Currently, ONYX’s NDI implementation is focused on inputting video/audio into ONYX rather than outputting ONYX’s own content as NDI. In other words, ONYX is an NDI receiver and not an NDI broadcaster (aside from possibly sending audio out via NDI in some future update, but that’s not a main feature as of 4.10). The phrase “NDI Streaming Video” in release notes refers to ONYX capturing video streams into Dylos, not ONYX outputting a video stream of its pixel engine
usitt.org
. However, you may still want to take the rich DYLOS generator patterns or compositions and use them as video content elsewhere (for example, displaying the pattern on an LED wall or in Resolume, in sync with lighting). There are a few strategies to achieve this even without native NDI output from ONYX:
Recreate or Share the Source: Many DYLOS generator effects are algorithmic (noise, plasma, etc.) and often similar algorithms exist in visual software. If you want the same pattern on lighting and video, you could generate it in software like TouchDesigner and send it to both: output as NDI to ONYX and directly play it on the LED wall. This way ONYX and the video wall use the identical content source.
Capture ONYX’s Output: ONYX doesn’t directly render a full-resolution video of the lighting output (since the “output” is DMX values). But if you have a visualizer or 3D view showing the lights, you could capture that. For instance, using a previz software like Capture connected to ONYX, you can then capture the video feed of Capture via NDI Tools (Newtek NDI Scan Converter or similar) and send that to a media server. This is more complex and usually only for preview or broadcast, not low-latency integration.
Spout/Syphon (Advanced PC integration): On PC, if you are running ONYX and a media program on the same machine, you might use the Spout framework to grab the DYLOS preview window (if accessible) and convert to NDI. This is an experimental approach and not officially supported by ONYX, but tools exist to capture a window as NDI.
Future ONYX Features: It’s worth noting ONYX is under active development, and the initial NDI support could be extended. The current documentation emphasizes input. Should ONYX allow outputting a DYLOS Zone as NDI in the future, the use case would be straightforward: e.g. send a low-res video of a lighting effect to an LED screen for perfectly matching visuals. Keep an eye on ONYX release notes for any mention of NDI output.
Despite ONYX not outputting NDI video directly, you can use the DMX output and NDI in tandem: For example, run the DYLOS content on lighting fixtures and simultaneously send a copy of that content (maybe via a media server) to video screens. With careful content design and maybe some calibration, lighting and video can appear unified.
Practical NDI Use Cases
Resolume to ONYX (Video Driven Lighting): A common integration is feeding a VJ’s output to ONYX so lights follow video content. Set Resolume to broadcast NDI (it can output its composition or a specific layer as NDI). ONYX ingests that NDI stream and maps it to an LED fixture grid via DYLOS. The result: if Resolume is playing a colorful animation, your lighting rig reproduces the same animation on your stage truss LEDs or wall washers. This was historically done with CITP media servers or by exporting video to pixel mapping software – NDI makes it real-time and network-based. Tip: In Resolume, use the same resolution for NDI as your Dylos zone pixel grid for 1:1 mapping, or use DYLOS scaling as needed.
Interactive Camera Feed: Place an NDI-enabled camera (or use NDI Virtual Input from a phone camera) pointed at the crowd. ONYX can take that feed and, say, map it to a low-res matrix of beam lights or pixel batons, creating a lo-fi “video wall” out of lights where you see the audience’s movement echoed by the rig. This could also feed into audio analysis (people moving = triggering sound via audio in NDI if there’s a mic).
ProPresenter Lyric Integration: Houses of worship often use ProPresenter for lyrics and backgrounds, which now supports NDI output. ONYX can grab a ProPresenter NDI output (which might be song lyrics over a colored background) and use it artistically in DYLOS (for instance, sampling colors from the slides to change lighting, or even projecting the words across fixtures). The American Cinematographer notes mention NDI enhancing compatibility with ProPresenter specifically
usitt.org
.
Audio Visualization: With ONYX’s audio input processors supporting NDI audio, you can send a DAW’s output or a DJ mix over NDI (via tools like Resolume or Reaper with NDI plugins
forum.obsidiancontrol.com
). ONYX can then generate a spectrum or waveform effect through DYLOS (e.g., an audio waveform running through a line of LED strip fixtures). This ties lighting effects tightly to the music without needing direct line-level audio input (useful if the lighting console is far from the audio source – just network them).
Having covered OSC, DMX, and NDI individually, let’s bring it all together with strategies for integrating ONYX into a larger show control system using all these methods.
Integration Strategies: Combining OSC, DMX, and NDI
The real power of ONYX in a production environment is realized when it works in concert with other systems – be it triggering lighting cues from a timeline, synchronizing lights with video content, or interactive installations. Here we discuss how to use OSC, DMX, and NDI together to integrate ONYX with visual software like Resolume and TouchDesigner, among others. We’ll outline a couple of example setups and best practices for a bidirectional control and monitoring environment with ONYX at the core.
ONYX + Resolume (Lighting and Video)
Scenario: A music show has a LED wall (controlled by Resolume Arena) and a lighting rig (controlled by ONYX). The designer wants some cues triggered from the lighting console to also affect video, and vice versa, and ensure lighting and visuals stay in sync.
NDI for Visual Sync: Resolume’s output (or a specific layer) is sent via NDI to ONYX. This could be abstract content (color waves, shapes) that DYLOS maps to LED pixel fixtures. When a certain video plays, the stage wash lights emulate the colors and movement from that video in real time. This creates a cohesive look where screens and lights share content. Configuration: Enable NDI on ONYX and select the Resolume NDI stream in an Input slot; apply it to a DYLOS zone covering relevant fixtures.
DMX for Control: ONYX can control Resolume using DMX. For instance, one universe is set aside for media control. In Resolume, map DMX channels to clip triggers or effects (Resolume supports Art-Net input natively). When the ONYX operator presses the “Strobe” cuelist, not only do the lights strobe, but an effect in Resolume is triggered via a DMX channel to add a strobe filter to the video. Conversely, if you want video to trigger lights: Resolume can output Art-Net as well. You could have a Resolume clip send a specific DMX value on Universe 10 channel 1 when it starts, which ONYX’s DMX Input mapping picks up to fire a corresponding lighting cue. For example, a clip of a flame could send a DMX trigger that makes ONYX run a fire-like lighting chase.
OSC for Cue Sync or Remote: If both systems support OSC, another method is to use OSC for high-level triggers. Resolume can be set to listen for OSC (or send OSC). In this integration, one might run a central timeline (Ableton, etc.) that sends OSC commands to both ONYX and Resolume to trigger cues simultaneously. However, without a central timeline, one could still let ONYX be the master: ONYX has a scripting system (through Lua or cues) that could send out UDP/OSC on a trigger (though ONYX doesn’t natively send arbitrary OSC, it can send Telnet/UDP as of 4.10 for triggers
usitt.org
). A workaround is running a small intermediate program that listens to ONYX’s OSC feedback (say when cuelist X goes, it receives an OSC from ONYX) and then that program issues an OSC command to Resolume to launch a clip. This is more advanced and typically not needed if DMX linking does the job.
Best Practice: When integrating ONYX with a media server like Resolume, decide which system is the “primary” controller for a given aspect. It’s often wise to let ONYX handle all timecode or show sequence (so lighting drives video or they’re both driven by timecode) – this way, a lighting operator can manually override if needed. Use NDI for content sync (lighting mimicking video) and use DMX/OSC for cue sync (ensuring actions on one trigger actions on the other). Always label your universes and keep a mapping documentation (e.g., Universe 50: Resolume Control – Channel 1: Clip1, Ch2: Clip2, etc.) so that both the lighting and video programmers know the linkage.
ONYX + TouchDesigner (Interactive Installations)
Scenario: A modern art installation has sensors feeding into a TouchDesigner patch which generates both visuals on projectors and wants to control lights via ONYX. The lights are complex to control (DMX moving heads, pixel strings), so ONYX is used for its fixture library and programming, but TouchDesigner will dictate when and how cues fire based on interactivity.
OSC Control from TD: TouchDesigner can send OSC messages directly to ONYX’s OSC input. For instance, if a person steps on a floor pad, TD triggers an OSC /Mx/playback/page1/1/go to ONYX to launch a spotlight cue. Because ONYX supports a rich set of OSC commands, TD can also fade lights by sending fader messages (like gradually sending /Mx/fader/4203 values to dim up/down a light over time). This allows generative or algorithmic control of ONYX cues without needing to program dozens of cuelists for every nuance – ONYX handles the heavy lifting of outputting correct DMX values, but TD decides when and to what level via OSC. Ensure ONYX’s OSC device is configured to accept TD’s IP and that TD is sending to the correct port.
DMX or OSC Feedback to TD: If the installation needs to react to what ONYX is doing (say change a visual element once a lighting cue completes), TD could either listen for OSC feedback from ONYX or even sample the lighting state via DMX. OSC feedback approach: ONYX will output fader and button states, but perhaps more useful is to use a dummy fixture on an unused DMX universe as a “communication channel.” For example, ONYX could have a cuelist that, when a sequence is done, sets a channel on Universe 90 to 255. TouchDesigner listens to sACN Universe 90, sees that value go high, and knows to advance to the next phase. This is essentially using DMX as a signaling mechanism. It may be simpler than parsing OSC if only a few triggers are needed, since TD has good DMX (sACN) support as well.
NDI for Visuals into ONYX: In an interactive environment, TouchDesigner might be generating visuals like particle systems or fractals. By broadcasting these as NDI, ONYX can take them into DYLOS so the lighting becomes another “screen” for the generated visuals. For instance, an interactive waveform in TD that reacts to sound can be NDI-fed to ONYX to drive a huge array of LED strip in sync with a projection. This ties the installation’s physical lighting and projection mapping together – both driven by the same real-time graphics. The system design would have TD handle all creative generation and ONYX handle output to fixtures and any additional lighting-specific effects layered on.
Best Practice: With interactive systems, latency is key. OSC and sACN are both low-latency; however, NDI for high-res video can introduce a bit of delay. If timing between light and projector visuals is critical, consider using lower resolution or the low-latency mode for NDI, or even alternate approaches (spouting pixel data directly via DMX if resolution is small enough). Also, throttle OSC messages from TD – for example, instead of sending every frame, maybe send 30 values per second for a smooth fade to avoid flooding ONYX. ONYX can generally handle frequent OSC, but unnecessary traffic can increase CPU usage.
Putting It All Together – A Unified Workflow
Imagine a complex show where ONYX is the central lighting console, Resolume runs content for LED walls, and TouchDesigner handles interactive sensors and generative effects. An example workflow leveraging all protocols could be:
Pre-show configuration:
ONYX is programmed with baseline lighting looks and cuelists (for stage washes, beams, etc.). It has an OSC device set up for TD (DeviceSpace 0 controlling main playbacks). EtherDMX is enabled for Universe 50 (Resolume control) and Universe 90 (feedback signals). NDI is enabled on the media network interface to receive video from Resolume or TD.
Resolume is programmed with video clips for each song and is set to output NDI (the full mix) and also listen on Art-Net universe 50 for certain triggers (e.g., Clip Advance on Channel 1).
TouchDesigner is built to handle sensor input (say Kinect or MIDI controllers). It will send OSC to ONYX when certain events occur (like people movement -> trigger cue). It also receives some OSC/DMX feedback from ONYX (to know when lights have finished a transition, etc.). TD also can send an output visual as NDI if it generates one, or it can composite Resolume’s NDI with additional effects and re-broadcast – depending on the design.
During the show:
At show start, ONYX receives a “Go” from a timecode system or operator, triggering the first cue (house lights dim). Simultaneously, TouchDesigner (if controlling show start) could have sent an OSC to Resolume to start playback of the first song visual. Alternatively, ONYX’s cue could have included a DMX trigger on universe 50 that Resolume picks up to start the clip.
As the band plays, a performer’s gesture is captured by TouchDesigner which decides to trigger an improvised lighting effect: it sends /Mx/playback/page1/5/go to ONYX to fire a pre-made strobe cue. Simultaneously, it flashes a graphical element on the LED wall via Resolume. The audience sees lights and visuals strobe together in response to the performer, even though that wasn’t a timed cue – it’s interactive.
Later, a break in the music is coming up, and the designer wants a synchronized blackout with a video cut. The lighting operator presses the “Blackout” cuelist on ONYX; ONYX outputs a DMX command that Resolume mapped to “Kill All Layers,” so video goes dark at the same moment lights go out. After the blackout, ONYX brings up a DYLOS effect using an NDI feed from Resolume (maybe a slow-motion replay or ambient graphic) across the lighting rig for a low-light ambiance during a quiet section.
Throughout, ONYX is streaming Art-Net, and a separate system or the lighting director’s console might be monitoring DMX values or using a visualizer for backup. If ONYX were to fail (worst-case), the Art-Net feed could be taken over by a backup console sending on the same universes – ONYX’s merge settings could allow that seamlessly if set up.
Post-show: All systems are stopped either manually or via a master OSC/UDP trigger that ONYX can now handle (for example, a central show controller could send a UDP “shutdown” command to ONYX which can be mapped to releasing all playbacks and to Resolume to fade out). ONYX’s new support for external triggers like Telnet/UDP means it can listen for a network message to execute a macro
usitt.org
, which is another avenue for integration (useful for theme parks or installations where a central scheduler triggers everything, including ONYX, over the network).
Integration Best Practices Summary:
Time Sync: If precise synchronization is needed (e.g., lip-sync between lights and video), consider using timecode or a common clock. ONYX can follow MIDI Timecode or even TCP timecode; Resolume can also follow timecode. This isn’t strictly necessary with OSC/DMX triggers if things are relatively close, but for long sequences, timecode ensures drift-free sync.
Redundancy: When multiple systems run together, plan what happens if one fails. ONYX merging DMX input means you can have a backup controller feed in if ONYX stops. Similarly, if NDI feed drops, have a fallback content in DYLOS (maybe a still image or a default generator) so lights aren’t left doing nothing. ONYX’s NDI node list allows you to quickly disable a problematic stream if needed
support.obsidiancontrol.com
.
Network Management: Use a robust network switch (gigabit or higher, with QoS if possible for NDI vs Art-Net). NDI can use a lot of bandwidth; it may benefit from enabling only the needed streams and perhaps using NDI’s lower bandwidth modes if available. The forum user experiences note it can take some seconds for ONYX to detect a new NDI stream
forum.obsidiancontrol.com
forum.obsidiancontrol.com
 – so start your NDI sources well before you need them live, to allow ONYX to lock on.
Documentation: Document all OSC addresses, DMX channel maps, and NDI sources used in the integration. This is more a project management tip, but it’s easy to forget which channel triggered which cue after programming dozens of them. Keep a simple table: e.g., “Universe 50: Ch1 = Video Strobe ON (255=on), Ch2 = Next Video, Ch3 = Prev Video, ...” and “OSC: /Mx/playback/page1/10/go = Pyro effect cue (triggered by TD when sensor X active)”.
By harnessing OSC for command/control, DMX for widespread compatibility and precision channel control, and NDI for rich media streaming, ONYX can be at the heart of a complex, interactive visual show system. Whether you are a developer extending a code-driven art performance or a show programmer linking consoles and servers, ONYX provides the hooks to make it all work together. Use the examples and practices above as a starting point to build your integrated lighting workflows, and refer to ONYX’s official documentation for further technical details and updates as the software evolves.