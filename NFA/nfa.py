
def citeste_fisier_config(nume_fisier):
    
    with open(nume_fisier, 'r') as f:
        continut = f.read()
    
    sectiuni = {}
    sectiune_curenta = None
    
    for linie in continut.split('\n'):
        linie = linie.strip()
        
        if not linie or linie.startswith('#'):
            continue
        
        if linie.startswith('[') and linie.endswith(']'):
            sectiune_curenta = linie[1:-1]
            sectiuni[sectiune_curenta] = []
            continue
        
        if sectiune_curenta:
            sectiuni[sectiune_curenta].append(linie)
    
    # Citeste alfabetul (Sigma)
    sigma = []
    if 'Sigma' in sectiuni:
        sigma = [s.strip() for s in sectiuni['Sigma'] if s.strip()]
    
    # Citeste starile si etichetele (S = start, F = final)
    stari = []
    stare_initiala = None
    stari_finale = []
    if 'States' in sectiuni:
        for stare in sectiuni['States']:
            if '=' in stare:
                nume, info = [p.strip() for p in stare.split('=', 1)]
                stari.append(nume)
                
                if 'S' in info:
                    if stare_initiala is None:
                        stare_initiala = nume
                    else:
                        raise ValueError("Exista mai multe stari initiale!")
                
                if 'F' in info:
                    stari_finale.append(nume)
            else:
                stari.append(stare.strip())
    
    # Citeste tranzitiile
    tranzitii = []
    if 'Transitions' in sectiuni:
        for tranz in sectiuni['Transitions']:
            parti = [p.strip() for p in tranz.split()]
            if len(parti) == 3:
                tranzitii.append(tuple(parti))
            else:
                raise ValueError(f"Tranzitie invalida: {tranz}")
    
    return sigma, stari, tranzitii, stare_initiala, stari_finale

def citeste_siruri_test(nume_fisier):
    """Citeste sirurile de test din fisier"""
    with open(nume_fisier, 'r') as f:
        return [linie.strip() for linie in f if linie.strip() and not linie.startswith('#')]

def inchidere_epsilon(stari_curente, tranzitii):
    """Calculeaza inchiderea epsilon pentru un set de stari"""
    inchidere = set(stari_curente)
    coada = list(stari_curente)
    
    while coada:
        stare = coada.pop()
        
        for (sursa, simbol, dest) in tranzitii:
            if sursa == stare and simbol == 'ε' and dest not in inchidere:
                inchidere.add(dest)
                coada.append(dest)
    
    return inchidere

def tranzitie_nfa(stari_curente, simbol, tranzitii):
    """Aplica o tranzitie pentru un simbol dat"""
    stari_noi = set()
    
    for stare in stari_curente:
        for (sursa, symb, dest) in tranzitii:
            if sursa == stare and symb == simbol:
                stari_noi.add(dest)
    
    return stari_noi

def ruleaza_nfa(sigma, stari, tranzitii, stare_initiala, stari_finale, sir_intrare):
    """Ruleaza NFA pe un sir de intrare"""
    for simbol in sir_intrare:
        if simbol not in sigma and simbol != 'ε':
            raise ValueError(f"Simbol '{simbol}' nu este in alfabet!")
    
    stari_curente = inchidere_epsilon([stare_initiala], tranzitii)

    for simbol in sir_intrare:
        stari_dupa_tranzitie = tranzitie_nfa(stari_curente, simbol, tranzitii)
        stari_curente = inchidere_epsilon(stari_dupa_tranzitie, tranzitii)

        if not stari_curente:
            return False

    # Verifica doar la final daca suntem intr-o stare finala
    return any(stare in stari_finale for stare in stari_curente)

def main():
    import sys
    
    if len(sys.argv) != 3:
        print("Folosire: python nfa_citire_fisier.py <fisier_config> <fisier_test>")
        print("Exemplu: python nfa_citire_fisier.py nfa_config.txt siruri_test.txt")
        return
    
    fisier_config = sys.argv[1]
    fisier_test = sys.argv[2]
    
    try:
        # Incarca configuratia NFA
        sigma, stari, tranzitii, stare_initiala, stari_finale = citeste_fisier_config(fisier_config)
        
        # Incarca sirurile de test
        siruri_test = citeste_siruri_test(fisier_test)
        
        print("\nConfiguratie NFA incarcata:")
        print(f"Alfabet (Sigma): {sigma}")
        print(f"Stari (Q): {stari}")
        print(f"Stare initiala: {stare_initiala}")
        print(f"Stari finale: {stari_finale}")
        print("Tranzitii:")
        for tranz in tranzitii:
            print(f"  {tranz[0]} --{tranz[1]}--> {tranz[2]}")
        
        print("\nRezultate testare:")
        for sir in siruri_test:
            try:
                rezultat = ruleaza_nfa(sigma, stari, tranzitii, stare_initiala, stari_finale, sir)
                print(f"Sirul '{sir}': {'ACCEPTAT' if rezultat else 'RESPINS'}")
            except ValueError as e:
                print(f"Sirul '{sir}': EROARE - {e}")
    
    except Exception as e:
        print(f"Eroare: {e}")

if __name__ == "__main__":
    main()