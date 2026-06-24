# -*- coding: utf-8 -*-
"""
Rodada calibrada (regime livre) para C1-C4 — Sprint 3, Equipe 2.

Objetivo: quantificar o teto de qualidade alcancavel por uma metaheuristica forte
e o quanto a configuracao CONTROLADA imposta (double-bridge + estrita, sem Swap,
100 iteracoes, seed 42) deixa sobre a mesa.

Motor: ILS com multi-restart aleatorio + busca local enriquecida
(2-opt intra + Relocate inter + Or-opt(2,3) + Swap inter + criacao de rota),
reotimizacao do tipo de veiculo por rota (escolhe o mais barato viavel) e
perturbacao mista (double-bridge / relocate aleatorio k=3). Avaliacao por delta
de custo nas rotas afetadas (rapido). Restricoes do problema real preservadas:
capacidade POR ROTA (FIO 650 kg / VUC 3000 kg) e jornada de 8 h POR ROTA.

Uso: py calibrado_c1_c4.py
"""
import json, random, time
from pathlib import Path
import numpy as np

BASE = Path(__file__).resolve().parents[2] / "2" / "datasets"
INST = {"C1": "Equipe_2_C1_10", "C2": "Equipe_2_C2_25",
        "C3": "Equipe_2_C3_40", "C4": "Equipe_2_C4_60"}
# Referencia: melhor ILS controlado por instancia (min entre trilhas NN/CW), README Aula11_ILS.
CONTROLADO = {"C1": 422.38, "C2": 710.47, "C3": 775.01, "C4": 1384.65}
QFIO, QVUC, FFIO, FVUC, CKM, V, H = 650.0, 3000.0, 250.0, 550.0, 1.5, 40.0, 8.0
# Orcamento por instancia (s). Instancias maiores exigem mais restarts para
# escapar de otimos locais ruins; a variancia entre restarts e alta em C3/C4.
SEC_POR_INST = {"C1": 20, "C2": 60, "C3": 200, "C4": 280}
MAX_RESTARTS = 400


def build(D, q, s):
    N = len(q); CUST = list(range(1, N))

    def rdist(r):
        if not r: return 0.0
        x = D[0, r[0]] + D[r[-1], 0]
        for i in range(len(r) - 1): x += D[r[i], r[i + 1]]
        return x

    def rload(r): return sum(q[c] for c in r)
    def rtime(r): return rdist(r) / V + sum(s[c] for c in r)

    def rcost(r):
        if not r: return 0.0
        if rtime(r) > H + 1e-6: return float("inf")
        l = rload(r); d = rdist(r)
        if l <= QFIO + 1e-6: return FFIO + CKM * d
        if l <= QVUC + 1e-6: return FVUC + CKM * d
        return float("inf")

    def veh(r): return "FIO" if rload(r) <= QFIO + 1e-6 else "VUC"
    def sol_cost(sol): return sum(rcost(r) for r in sol)
    def clean(sol): return [r for r in sol if r]

    def two_opt(r):
        best = r[:]; bd = rdist(best); imp = True
        while imp:
            imp = False
            for i in range(len(best) - 1):
                for k in range(i + 1, len(best)):
                    cand = best[:i] + best[i:k + 1][::-1] + best[k + 1:]
                    cd = rdist(cand)
                    if cd < bd - 1e-6 and rtime(cand) <= H + 1e-6:
                        best, bd = cand, cd; imp = True; break
                if imp: break
        return best

    def local_search(sol):
        sol = clean([r[:] for r in sol]); imp = True
        while imp:
            imp = False
            for i in range(len(sol)):
                nr = two_opt(sol[i])
                if rdist(nr) < rdist(sol[i]) - 1e-6: sol[i] = nr; imp = True
            if imp: continue
            cost = [rcost(r) for r in sol]; done = False
            for a in range(len(sol)):
                for ci in range(len(sol[a])):
                    cust = sol[a][ci]; ra2 = sol[a][:ci] + sol[a][ci + 1:]; ca2 = rcost(ra2)
                    if ca2 == float("inf"): continue
                    for b in range(len(sol)):
                        if b == a: continue
                        rb = sol[b]
                        for pos in range(len(rb) + 1):
                            rb2 = rb[:pos] + [cust] + rb[pos:]; cb2 = rcost(rb2)
                            if cb2 == float("inf"): continue
                            if ca2 + cb2 < cost[a] + cost[b] - 1e-6:
                                sol[a] = ra2; sol[b] = rb2; sol = clean(sol); imp = True; done = True; break
                        if done: break
                    if done: break
                    if rcost([cust]) + ca2 < cost[a] - 1e-6:
                        sol[a] = ra2; sol.append([cust]); sol = clean(sol); imp = True; done = True; break
                if done: break
            if imp: continue
            for L in (2, 3):
                for a in range(len(sol)):
                    if len(sol[a]) < L: continue
                    for ci in range(len(sol[a]) - L + 1):
                        seg = sol[a][ci:ci + L]; ra2 = sol[a][:ci] + sol[a][ci + L:]; ca2 = rcost(ra2)
                        if ca2 == float("inf"): continue
                        for b in range(len(sol)):
                            if b == a: continue
                            rb = sol[b]
                            for pos in range(len(rb) + 1):
                                for sg in (seg, seg[::-1]):
                                    rb2 = rb[:pos] + sg + rb[pos:]; cb2 = rcost(rb2)
                                    if cb2 == float("inf"): continue
                                    if ca2 + cb2 < cost[a] + cost[b] - 1e-6:
                                        sol[a] = ra2; sol[b] = rb2; sol = clean(sol); imp = True; done = True; break
                                if done: break
                            if done: break
                        if done: break
                    if done: break
                if done: break
            if imp: continue
            for a in range(len(sol)):
                for b in range(a + 1, len(sol)):
                    for ia in range(len(sol[a])):
                        for ib in range(len(sol[b])):
                            ra2 = sol[a][:]; rb2 = sol[b][:]; ra2[ia], rb2[ib] = rb2[ib], ra2[ia]
                            ca2, cb2 = rcost(ra2), rcost(rb2)
                            if ca2 + cb2 < cost[a] + cost[b] - 1e-6:
                                sol[a] = ra2; sol[b] = rb2; imp = True; done = True; break
                        if done: break
                    if done: break
                if done: break
        return clean(sol), sol_cost(clean(sol))

    def dbridge(r, rng):
        n = len(r)
        if n < 4: return r[:]
        a, b, c = sorted(rng.sample(range(1, n), 3)); return r[:a] + r[b:c] + r[a:b] + r[c:]

    def perturb(sol, rng, k):
        ns = [r[:] for r in sol]; m = rng.random()
        if m < 0.5:
            elig = [i for i, r in enumerate(ns) if len(r) >= 4]
            if elig: j = rng.choice(elig); ns[j] = dbridge(ns[j], rng)
            else: m = 1.0
        if m >= 0.5:
            for _ in range(k):
                elig = [i for i, r in enumerate(ns) if len(r) >= 2]
                if not elig: break
                a = rng.choice(elig); cust = ns[a].pop(rng.randrange(len(ns[a])))
                b = rng.randint(0, len(ns))
                if b >= len(ns): ns.append([cust])
                else: ns[b].insert(rng.randint(0, len(ns[b])), cust)
                ns = clean(ns)
        return ns if all(rcost(r) < float("inf") for r in ns) else [r[:] for r in sol]

    def ils(init, seed, iters, k):
        rng = random.Random(seed); cur, cc = local_search(init); best = [r[:] for r in cur]; bc = cc
        for _ in range(iters):
            cand, cc2 = local_search(perturb(cur, rng, k))
            if cc2 < cc - 1e-6: cur, cc = cand, cc2
            if cc2 < bc - 1e-6: best, bc = [r[:] for r in cand], cc2
        return best, bc

    def random_init(rng):
        order = CUST[:]; rng.shuffle(order); routes = []; cur = []; load = 0
        for c in order:
            if load + q[c] <= QFIO and rtime(cur + [c]) <= H: cur.append(c); load += q[c]
            else:
                if cur: routes.append(cur)
                cur = [c]; load = q[c]
        if cur: routes.append(cur)
        return routes

    return ils, random_init, rcost, veh, rdist, rload, rtime, sol_cost


def main():
    print("Rodada calibrada (regime livre) — C1-C4 | Equipe 2 / Grupo 2\n")
    out = []
    for name, folder in INST.items():
        D = np.load(BASE / folder / "D.npy"); q = np.load(BASE / folder / "q.npy"); s = np.load(BASE / folder / "s.npy")
        ils, random_init, rcost, veh, rdist, rload, rtime, sol_cost = build(D, q, s)
        t0 = time.time(); best = None; bc = float("inf"); n = 0
        budget = SEC_POR_INST[name]
        while time.time() - t0 < budget and n < MAX_RESTARTS:
            sol, c = ils(random_init(random.Random(5000 + n)), n, 200, 3); n += 1
            if c < bc - 1e-9: best, bc = sol, c
        ctrl = CONTROLADO[name]; ganho = (ctrl - bc) / ctrl * 100
        assert sorted(c for r in best for c in r) == list(range(1, len(q))), "inviavel: cobertura"
        assert all(rcost(r) < float("inf") for r in best), "inviavel: cap/jornada"
        rotas = [{"vehicle": veh(r), "n_clientes": len(r), "carga_kg": round(rload(r), 1),
                  "dist_km": round(rdist(r), 2), "tempo_h": round(rtime(r), 2),
                  "route": [0] + r + [0]} for r in best]
        out.append({"instancia": name, "controlado_rs": ctrl, "calibrado_rs": round(bc, 2),
                    "ganho_pct": round(ganho, 2), "n_restarts": n, "n_rotas": len(best), "rotas": rotas})
        print(f"{name}: controlado R$ {ctrl:8.2f} | calibrado R$ {bc:8.2f} | ganho {ganho:+5.2f}% "
              f"| {len(best)} rotas {[veh(r) for r in best]} | {n} restarts")
    Path(__file__).with_name("calibrado_c1_c4_resultado.json").write_text(
        json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    print("\nResumo salvo em calibrado_c1_c4_resultado.json")


if __name__ == "__main__":
    main()
