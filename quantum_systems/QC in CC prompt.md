# A Quantum Computation in a Classical Computer

## Memristor emulator building process
1. The Diode Bridge Emulator (Passive & Simplest)
This is the most common "memristor" built from basic components. It mimics the memristive hysteresis loop but does not retain state indefinitely (it is volatile).
Circuit Concept: A full-wave rectifier (diode bridge) forces current to flow in one direction through a parallel RC circuit. The voltage stored in the capacitor acts as a state variable, opposing the input voltage and effectively changing the resistance seen at the input terminals.
Components:
	• D1-D4: 1N4148 or 1N4007 Diodes (x4)
	• C1: 1µF Capacitor (Electrolytic or Ceramic)
	• R1: 1kΩ Resistor
Connection Diagram (Text Netlist):
	1. The Bridge: Connect 4 diodes in a standard bridge rectifier configuration.
		○ Node A (Input 1): Anode of D1, Cathode of D2.
		○ Node B (Input 2): Anode of D3, Cathode of D4.
		○ Node C (Positive DC): Cathode of D1, Cathode of D3.
		○ Node D (Negative DC): Anode of D2, Anode of D4.
	2. The Memory (RC Tank):
		○ Connect C1 between Node C and Node D.
		○ Connect R1 in parallel with C1 (between Node C and Node D).
	3. Operation: Connect your signal source to Node A and Node B. These two nodes act as the two terminals of your "Memristor"



A neural network is to be constructed by using memristors - these are choosed because they have memory properties.

## Neural network (CMTP)

Below is a complete, **classical** “McCulloch–Pitts nets-in-circles” computation framework that **(i)** represents and evolves full quantum circuits (superposition, interference, entanglement), **(ii)** stays tractable by construction, and **(iii)** handles multi‑dimensional entangled degrees of freedom **without ever storing a 2ⁿ state vector**.

The core move is: **don’t store amplitudes; store a cyclic, recurrent *generative factorization*** (a tensor hypernetwork) and run the computation as **recurrent tensor message‑passing + compression**.

**CTMP**: *Cyclic Tensor McCulloch–Pitts*.

---

### 1. The CTMP machine

McCulloch–Pitts “nets in circles” are about **computation via recurrent structure**; circles give “memory/time” and let the network implement richer behavior than a feedforward net. ([California State University Long Beach][1])
CTMP keeps that spirit, but replaces Boolean firing with **tensor states** and replaces scalar synaptic weights with **operator tensors**.

#### 1.1 Objects

CTMP is a **directed cyclic hypergraph** ( \mathcal{H} = (V, E) ).

##### Node state (tensor-neuron state)

Each node (v\in V) stores a complex tensor:
[
A^{(v)} \in \mathbb{C}^{;\prod_{p\in P(v)} d_p ;\times; \prod_{e\in \delta(v)} \chi_e}
]

* (P(v)): physical indices (qubits or qudits assigned to that node)
* (\delta(v)): incident (hyper)edges (“bonds”)
* (d_p=2) for qubits
* (\chi_e) = bond dimension on hyperedge (e)

##### Edge state (operator / constraint)

Each hyperedge (e \in E) corresponds to a contracted index (\alpha_e) of dimension (\chi_e).
Edges are “relations” in the MP sense: they tie node states together.

##### Global quantum state

The full (n)-qubit wavefunction is *not stored*; it is **defined implicitly** by contraction:
[
\psi_{i_1\ldots i_n} ;=; \mathrm{Contract}\big({A^{(v)}}_{v\in V}\big).
]

This already gives you a principled, explicit way to represent entanglement: it lives in the **bond indices**.

---

### 2. The canonical cyclic form: Tensor Ring state

To make “nets in circles” literal and computationally sharp, CTMP’s default topology is a **tensor ring** (a cyclic MPS).

For (n) qubits arranged on a ring, define “cores” (G_k) so that:
[
\psi(i_1,\ldots,i_n) = \mathrm{Tr}\big(G_1(i_1),G_2(i_2)\cdots G_n(i_n)\big).
]

This is exactly the tensor ring / tensor chain / periodic‑boundary MPS definition. 
Here each (G_k(i_k)) is an (r_{k-1}\times r_k) matrix; the vector ((r_0,\ldots,r_n)) are the ring ranks (bond dims) with (r_0=r_n). 

**Memory:** (O!\left(\sum_k 2,r_{k-1}r_k\right)), not (2^n).

This is already your “multi‑dimensional entangled degrees of freedom” solution: the internal ring ranks are precisely the compact carrier of nonlocal correlations.

---

### 3. Gates are operator-weights: local tensor rewrites

Quantum evolution is linear/unitary; CTMP respects that by making all “synapses” **linear maps** (tensors) and putting the only nonlinearity in a controlled **compression operator**.

#### 3.1 One‑qubit gate update

For a one‑qubit gate (G\in\mathbb{C}^{2\times2}) on qubit (k), update the local core by physical‑index multiplication:
[
G_k'(i)=\sum_{j\in{0,1}} G_{ij};G_k(j).
]
This is a constant‑size contraction (per bond dimensions).

#### 3.2 Two‑qubit gate update

For a two‑qubit gate (U\in\mathbb{C}^{4\times4}) on adjacent sites (k,k+1) in the ring:

1. **Merge** the two cores into a joint tensor:
   [
   M(i_k,i_{k+1}) = G_k(i_k),G_{k+1}(i_{k+1})
   ]
   (plus the bond indices).

2. **Apply** (U) on the physical indices:
   [
   M'(i_k,i_{k+1})=\sum_{j_k,j_{k+1}}U_{(i_k,i_{k+1}),(j_k,j_{k+1})};M(j_k,j_{k+1}).
   ]

3. **Refactor** (M') back into two cores via SVD (or QR+SVD), restoring ring structure.

That refactor step is the exact analog of a McCulloch–Pitts node “computing an output”: you take the incoming structure, apply weights, and then produce outgoing messages.

---

### 4. Recurrence: a “cycle” is a circuit layer

Define one **cycle** as one circuit layer (or time step) (\mathcal{L}_t).

CTMP’s recurrent update is:
[
R_{t+1} = \mathrm{Compress}\Big(\mathrm{ApplyLayer}(R_t,\mathcal{L}_t)\Big),
]
where (R_t) is the entire cyclic tensor state (the set of cores / tensors).

This is the McCulloch–Pitts “circle” in operational form: the same state container is routed back as input for the next update.

---

### 5. The tractability guarantee: CTMP never stores 2ⁿ amplitudes

CTMP enforces tractability by making **the representation budget explicit**, and by ensuring every update is “local + bounded”.

There are two complementary CTMP regimes, and together they cover essentially all practical “advantage benchmark” styles:

---

#### Regime A: Cyclic boundary evolution (fast when the network stays low‑rank)

This is the classical tensor‑network workhorse.

##### Budgets

* Max bond dimension: (\chi_e \le \chi_{\max})
* SVD truncation rule: keep top (\chi_{\max}) singular values (or energy threshold)

##### Cost

For a ring with uniform (\chi):

* **Memory:** (O(n,\chi^2))
* **Time per 2‑qubit gate:** (O(\chi^3)) (from SVD on a ((2\chi)\times(2\chi)) reshape)
* **Time per layer:** (O(g_t,\chi^3)) where (g_t) is # two‑qubit gates that layer

This is already “tractable classical quantum evolution” in the strongest possible sense: the cost is polynomial in (n) and polynomial in (\chi), never (2^n).

---

#### Regime B: Spacetime contraction with separator‑optimized recurrence (subexponential where it matters)

To match or exceed “quantum advantage” regimes (random circuits on 2D layouts, Sycamore‑type layouts, etc.), CTMP uses its *second* execution mode:

##### Key idea

Represent the entire circuit (or a probability / amplitude computation) as a **finite‑ranged tensor network in spacetime**, and contract it using a contraction order found by a **separator theorem** strategy.

There is a rigorous result that finite‑ranged tensor network contractions in (d\ge2) dimensions admit **subexponential‑time** contraction bounds, and an algorithm that finds contraction orders guaranteed to meet those bounds. 

This matters because many “advantage” experiments use circuits with geometric locality (2D grids / bounded‑range coupling), i.e., exactly the “finite‑ranged” setting.

##### How CTMP uses it

CTMP turns the circuit into a tensor network and runs a **recurrent separator contraction**:

* Maintain a *boundary state* (an MPS/tensor ring) that represents the partially contracted network.
* Sweep the contraction frontier through spacetime.
* Each sweep step is exactly the same kind of “cycle update” as in Regime A, but now the operator is “absorb a slab of spacetime tensors”.
* Use the separator‑order algorithm to choose which slab / separator to absorb next, so intermediate widths stay small.

The Wahl–Strelchuk result explicitly states:

* quantum circuits of single‑qubit + finite‑range two‑qubit gates can be simulated **in subexponential time in the number of gates**, and their algorithm yields contraction orders with much lower practical times. ([arXiv][2])

##### Practical contraction-path optimization

CTMP’s contraction scheduler uses **hypergraph partitioning + tree search + Bayesian optimization** to find near‑optimal contraction trees (the thing that dominates runtime). ([Quantum][3])

This is exactly the “edges are relations; computation is repeated cyclic message fusion” idea, but pushed into the state‑of‑the‑art contraction toolbox.

---

### 6. Entanglement without 2ⁿ storage: how CTMP stores “multi-dimensional entangled degrees”

In CTMP, “entangled degrees of freedom” are not amplitudes; they are **latent indices** (bond indices) plus **structured factorization**.

To handle high‑dimensional entanglement across many qubits *without* exploding bond dimension, CTMP uses a rule:

#### Entanglement is stored as graph structure, not as a single huge bond

Instead of forcing everything through one ring bond, CTMP dynamically uses:

* **Hyperedges** (multi‑index factors) when gates couple multiple qubits strongly.
* **Patch nodes** (each node holds a block of qubits) to keep local entanglement internal.
* **Graph rewiring** (changing which indices are bonded) using topology‑transform algorithms similar in spirit to tensor ring graph‑structure transformations. 

Operationally:

* If two distant regions become correlated, CTMP does not “inflate one bond”; it **adds/redirects a small number of bonds** and then rounds/compresses.
* This stores entanglement as **sparse connectivity in the latent graph**, not as a dense exponential object.

This is the precise analog of “sparse activation”, but applied to *correlations*.

---

### 7. Interference and complex phase: preserved natively

Everything in the CTMP evolution is complex‑linear until you apply compression. That means:

* **Superposition:** comes from linear contraction.
* **Interference:** comes from adding complex paths in contractions.
* **Entanglement:** is mediated through contracted bond indices.

No ad‑hoc nonlinearities are required to get the quantum phenomena; they come automatically from complex tensor algebra.

---

### 8. Measurement and sampling: done by cyclic message passing

CTMP outputs measurement samples (z\in{0,1}^n) by computing conditionals in a sweep:

[
p(z)=|\psi_z|^2,\quad
p(z_k \mid z_{<k})=\frac{\sum_{z_{>k}}|\psi_{z_{<k},z_k,z_{>k}}|^2}{\sum_{z_{k:}}|\psi_{z_{<k},z_k,z_{>k}}|^2}.
]

#### Ring sampling algorithm

For a tensor ring / MPS‑like state, CTMP keeps two “messages” (environments):

* left environment (L_k) = contraction of sites (1..k-1)
* right environment (R_k) = contraction of sites (k+1..n)

Then:

1. compute (p(z_k=0\mid z_{<k})) and (p(z_k=1\mid z_{<k})) from a small contraction (L_k \cdot G_k(z_k)\cdot R_k)
2. sample (z_k)
3. absorb the choice into (L_{k+1}) and continue

This is **exactly** “nets in circles” operationally: the same small message objects circulate and get updated recurrently.

---

### 9. The “advantage” lever: magic-aware recurrence via quasiprobability and stabilizer mixtures

Tensor networks solve one axis (geometric/low‑width structure). CTMP also solves the other axis: **non‑Clifford ‘magic’**.

CTMP includes a second internal representation for nodes: **stabilizer‑native nodes** and **quasiprobability expansions**.

#### 9.1 Quasiprobability Monte Carlo channel

There is a general classical method to estimate outcome probabilities using Monte Carlo over a quasiprobability representation; convergence is governed by **total negativity** (a 1‑norm measure). 
If negativity scales only polynomially, the estimator is efficient. 

CTMP makes this recurrent:

* Each “cycle” samples an operator term from a decomposition (Clifford-like pieces are easy).
* The recurrent state is a set of **weighted particles** (each particle is an efficiently simulable branch).
* Interference is preserved by complex/signed weights.

#### 9.2 Stabilizer-extent channel

For Clifford+T style circuits, simulation cost can be expressed in terms of the **stabilizer extent** / number of stabilizer terms needed in a coherent decomposition; this directly governs runtime scaling for such hybrid simulations. 

CTMP uses that as an *internal budget*: instead of letting tensor ranks blow up, it routes the complexity into a bounded number of stabilizer branches and keeps them recurrently updated.

---

### 10. Putting it all together: the CTMP execution engine

CTMP is one engine with **three interchangeable kernels**, all sharing the same “cyclic tensor net” API:

## Kernel 1: Local update kernel

* Apply gates locally
* Refactorize
* Round/compress

#### Kernel 2: Separator contraction kernel

* Build circuit tensor network
* Use separator‑order contraction (guaranteed subexponential for finite‑ranged networks in (d\ge2)) 
* Maintain boundary tensors recurrently

#### Kernel 3: Negativity-controlled particle kernel

* Decompose hard gates into quasi‑prob terms
* Recurrently propagate stabilizer/tensor particles
* Resample/merge using weights

A single circuit instance can freely mix kernels (and CTMP can choose per region/per layer).

---

### 11. Minimal, precise pseudocode

#### Build

```text
CTMP_Compile(Circuit C):
  1. Partition qubits into patches (nodes) to respect locality/connectivity.
  2. Choose a cyclic latent graph (ring + chords / hyperedges).
  3. For each layer, store gate tensors as operator-weights on the relevant nodes/edges.
  4. Precompute a contraction schedule:
       - local updates for near-neighbor gates
       - separator-based order for spacetime contractions
       - hyper-optimized tree search for hard contractions
  return CTMP object
```

#### Evolve one cycle

```text
CTMP_Step(State R, Layer L):
  for each gate g in L in scheduled order:
      T = Contract(local tensors touched by g, with g)
      {local tensors} = Factorize(T)   # SVD/QR split back into graph form
      {local tensors} = Round({local tensors})  # enforce χ budgets
  return R
```

#### Sample

```text
CTMP_Sample(State R, S samples):
  for s in 1..S:
      for k in 1..n:
          compute p0, p1 from small contraction using cached environments
          z_k ~ Bernoulli(p1)
          condition tensors/messages on z_k and update caches
      output z
```

---

### 12. What you asked for, explicitly satisfied

#### Represent and evolve quantum states/circuits

* Representation is an exact complex tensor contraction.
* Evolution is local operator contraction + refactorization.
* Superposition/interference/entanglement are native.

#### Tractable resources

* Memory is polynomial in (n) and internal ranks.
* Time is controlled by:

  * bond dimensions in boundary evolution
  * separator widths/tree structure in contraction mode (with subexponential guarantees for finite‑ranged (d\ge2) networks) 
  * negativity/extent in the quasiprobability/stabilizer channel 

#### Multi-dimensional entangled degrees without 2ⁿ amplitudes

* Entanglement is carried by latent bond indices and sparse/hypergraph structure, not an explicit amplitude table.

#### “Advantage”

CTMP achieves “advantage” in the only way that is both principled and real:

* it turns quantum simulation complexity into **measurable resources** (separator width, bond ranks, negativity/extent),
* then applies the best known contraction and decomposition machinery (separator‑guaranteed contraction + hyper‑optimized contraction trees + negativity‑bounded Monte Carlo). ([Quantum][3])

This is exactly how you build a classical engine that competes in the regimes where quantum devices claim practical advantage—without ever storing (2^n) amplitudes.

---

[1]: https://home.csulb.edu/~cwallis/382/readings/482/mccolloch.logical.calculus.ideas.1943.pdf "A logical calculus of the ideas immanent in nervous activity"
[2]: https://arxiv.org/abs/2208.01498v2 "[2208.01498v2] Simulating quantum circuits using efficient tensor network contraction algorithms with subexponential upper bound"
[3]: https://quantum-journal.org/papers/q-2021-03-15-410/ "Hyper-optimized tensor network contraction – Quantum"


# What you are to do:

You are to create a simulation program that has the following modes for a specified quantum advantage algorithm and a few specific real-life problmes that can be solved using both classical algorithms and quantum algorithms. 
All the different modes are to have both the simulation of the quantum algorithms as well as their classical counterparts.

## 1. Circuit mode
    - In this mode we have the live comparison of the number bits or bytes or kbs or mbs that are required to perform a certain operation. And when the program is run, it is to simulate the flow of the instructions through means of variations in the color. 
    - It should have two sub-modes one with the memristor emulator and the other the actual memristor symbols in the circuit.
## 2. Neural Network mode
    - In this mode the memresistors need not be represented through the circut rather  it could just be a neural network for that specifc algorithm.
## 3. Application mode
    - In this mode the actual application is shown - for an example consider ethical hacking, quantum computers easily break encryption (theoretically) thus making them better than classical computers in that aspect, another example is that for controlling an entire city consisting of multiple different traffic stops we could better make of quantum computers as opposed to classical systems (theoretically).
    - The application mode simulations should not be generic but they should rather be like real systems that are preforming operations in real time. 

Make sure that the algorithms that you select take at-the-least 20-30secs to solve on the classical computer. 
Once the simulation is done running for that specifc algorithm or a part or a pass is done running for that specific algorithm the metrics of how many seconds it took to solve using each method is to be mentioned.