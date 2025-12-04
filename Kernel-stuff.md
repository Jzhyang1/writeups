Microkernel:
* WindowsNT, Mach are successful but they hybridize it with added drivers to reduce overhead

### Formally verified kernel
Rust has `Verus`

### Loadable Kernel Module (DLKM)

#### History

* some ELF files can have incomplete references that look like in-kernel references that the kernel can resolve at runtime, so the kernel can dynamically load it in
* Used often for device drivers and occasionally adds new system calls

#### Sandboxing 1: Task isolation

Create a process that has more IPC ports that can ask for more things quickly. IPC is implemented efficiently by using mmap to transfer data: mostly to acquire io-mappings.

#### Sandboxing 2: Emulating

Ex: eBPF
Scan thru the user code that checks to make sure that all code will be in permissions. This is done via a JIT-like runtime. 

Now, WASM can be used within the kernel

### Event Driven Kernel

No preemption within the kernel, everything runs from start-to-finish quickly
No stacks other than the per-core stacks

### Things drivers are needed for

Low-level: Disk, NIC, GPU, Keyboard, Mouse, USB, Audio
High-level: Pseudo-tty, special inodes, Mixer (e.g. Alsa), Graphics

### Trusted Platform Module (TPM)

* Hardware that verifies digital signatures of programs (i.e. kernel, encrypted file systems)

### X11

A protocol where a program runs and listens on a port/socket and all other programs who want to do graphics connect and follow the protocol to draw stuff on their window