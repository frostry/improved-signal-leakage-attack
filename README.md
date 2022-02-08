# Signal Leakage Attack using Targeted Signal Extraction

This software implements a signal leakage attack against the protocols DXL [DXL12], DBS [DBS19], and LBA-PAKE [DBK21].

The attack is in line with Fluhrers attack [Flu16] that has been improved by Ding, Alsayigh, Saraswathy, Fluhrer, and Lin [DAS+17] and Bindel, Stebila, and Veitch [BSV21] and improves upon them further. More concretely, it views signals as binary codes, enabling a 'target signal extration' approach. Our results caution against underestimating the power of signal leakage attacks.

Run attacks against DXL [DXL12]:
- `make`
- `python3 imp-dxl-pv.py`
- for comparing with the attack [BSV21], run `python3 compare-dxl.py`

Run attacks against DBS-KE [DBS19]:
- `make CFLAGS="-DVERS=19 -DN=512 -DSTDDEV=41915"`
- run `python3 imp-dbs-ke-pv.py 512`
- for comparing with the attack [BSV21], run `python3 compare-dbs-ke.py`

Run an attack against LBA-PAKE [DBK21]:
- `make CFLAGS="-DVERS=21"`
- run `python3 imp-lbapake-pv.py`

For Quantum2FA [WWC+21], we modify the code of [Newhope](https://github.com/newhopecrypto/newhope) to simulate the attack. To run it:
- `cd Quantum2FA`
- `make && ./test_cpakem512`

## Bibliography
[BSV21] Bindel, N., Stebila, D., Veitch, S.: Improved attacks against key reuse in learning with errors key exchange. In: LATINCRYPT 2021. LNCS, Springer (2021)

[DAS+17] Ding, J., Alsayigh, S., Saraswathy, R., Fluhrer, S., Lin, X.: Leakage of signal function with reused keys in RLWE key exchange. In: ICC 2017. pp. 1–6. IEEE (2017)

[DBK21] V. Dabra, A. Bala and S. Kumari, "LBA-PAKE: Lattice-Based Anonymous Password Authenticated Key Exchange for Mobile Devices," in IEEE Systems Journal, vol. 15, no. 4, pp. 5067-5077, Dec. 2021

[DBS19] Ding, J., Branco, P., Schmitt, K.: Key Exchange and Authenticated Key Exchange with Reusable Keys Based on RLWE Assumption. Cryptology ePrint Archive, Report 2019/665 (2019)

[DXL12] Ding, J., Xie, X., Lin, X.: A Simple Provably Secure Key Exchange Scheme Based on the Learning with Errors Problem. Cryptology ePrint Archive, Report 2019/688
(2012)

[Flu16] Fluhrer, S.R.: Cryptanalysis of ring-LWE based key exchange with key share reuse. Cryptology ePrint Archive, Report 2016/085 (2016)

[WWC+21] Q. Wang, D. Wang, C. Cheng and D. He, "Quantum2FA: Efficient Quantum-Resistant Two-Factor Authentication Scheme for Mobile Devices," in IEEE Transactions on Dependable and Secure Computing,
