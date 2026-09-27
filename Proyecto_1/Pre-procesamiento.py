#Parte 1

def pre_procesar_cuentas(lista_cuentas):
    cuentas_procesadas = []
    numeros_de_cuentas_vistos = []

    for cuenta in lista_cuentas:
        # (and) En el caso que si haya titular pero no haya un nombre
        if "titular" in cuenta and cuenta["titular"].strip() != "" and "numero_cuenta" in cuenta:
            #Limpiamos los espacios y ponemos la primera letra en mayuscula
            titular_limpio = ""

            for palabra in cuenta["titular"].strip().split():
                titular_limpio = titular_limpio + palabra.capitalize() + ""

            titular = titular_limpio.strip()

            #Conversion de cualquier tipo de dato a txt
            numero_de_cuenta_txt = str(cuenta["numero_cuenta"]).strip()

            try:
                numero_cuenta = int(numero_de_cuenta_txt)

                if numero_cuenta in numeros_de_cuentas_vistos:
                    print(f"Fallido al cargar la cuenta; (numero_cuenta {numero_cuenta} duplicado)")
                else:
                    #Verificamos el saldo inicial
                    try:
                        saldo_inicial = int(cuenta["saldo_inicial"])

                        if saldo_inicial < 0:
                            print(f"Error al cargar la cuenta; (saldo_inicial {saldo_inicial} es negativo)")

                        else:
                            #Verificamos el tipo de cuenta (Corriente o Ahorro)
                            tipo = str(cuenta.get("tipo", "")).strip().lower()

                            if tipo == "ahorro" or tipo == "corriente":
                                numeros_de_cuentas_vistos.append(numero_cuenta)

                                cuenta_limpia = {
                                    "titular": titular,
                                    "numero_cuenta": numero_cuenta,
                                    "saldo_inicial": saldo_inicial,
                                    "tipo": tipo
                                }

                                if tipo == "ahorro":
                                    try:
                                        tasa_interes = float(cuenta.get("tasa_interes"))
                                        if tasa_interes < 0:
                                            tasa_interes = 0.5

                                    except (ValueError, TypeError):
                                        tasa_interes = 0.5

                                    cuenta_limpia["tasa_interes"] = tasa_interes

                                else:
                                    try:
                                        limite_giro = int(cuenta.get("limite_giro"))
                                        if limite_giro < 0:
                                            limite_giro = 100000

                                    except (ValueError, TypeError):
                                        limite_giro = 100000

                                    cuenta_limpia["limite_giro"] = limite_giro


                                cuentas_procesadas.append(cuenta_limpia)
                                print(titular, "-->", numero_cuenta, "-->", saldo_inicial, "-->", tipo)

                            else:
                                print(f"Fallido al cargar la cuenta; (tipo '{tipo}' no valido)")
                    
                    except (ValueError, KeyError):
                        print("Fallido al cargar la cuenta; (saldo_inicial no es un numero)")

            except ValueError:
                print("Fallido al cargar la cuenta; (numero_cuenta no valido)")

        else:
            print("Fallido al cargar la cuenta; (Titular no registrado)")
    
    return cuentas_procesadas

datos_prueba = [
    {"titular": "Ana maria", "numero_cuenta": 101, "saldo_inicial": 5000, "tipo": "ahorro"},
    {"titular": "jUAN CARLOS", "numero_cuenta": "102", "saldo_inicial": "3000", "tipo": "corriente"},
    {"titular": "benjamin hernandez", "numero_cuenta": "103", "saldo_inicial": 1000, "tipo": "corriente"},
    {"titular": "YANIRA MANSILLA", "numero_cuenta": "104", "saldo_inicial": "10000", "tipo": "corriente"},
    {"titular": "EbAn dElGaDo", "numero_cuenta": 105, "saldo_inicial": "0", "tipo": "ahorro"},
    {"titular": "PABLO seron", "numero_cuenta": "abc", "saldo_inicial": 5, "tipo": "corriente"}, #descarte por invalidez (numero_cuenta)
    {"titular": "Ary Seron", "numero_cuenta": "102", "saldo_inicial": "10000", "tipo": "corriente"}, #descarte por duplicacion (numero_cuenta)
    {"titular": "ROcky SeRon", "numero_cuenta": "106", "saldo_inicial": "-500", "tipo": "ahorro"}, #descarte por numero negatico (saldo_inicial)
    {"titular": "Elena Molina", "numero_cuenta": "107", "saldo_inicial": "xyz", "tipo": "ahorro"}, #descarte por invalidez (saldo_inical)
    {"titular": "Pepito perez", "numero_cuenta": "108", "saldo_inicial": "500", "tipo": "empresarial"}, #descarte por tipo de cuenta
    {"titular": "Ariel Masle", "numero_cuenta": "109", "saldo_inicial": "100000", "tipo": "AHORRO"},
    # --- Registros nuevos (pedidos a claude para rellenar los demas casos pq me estaba demorando mucho :c) ---
    {"titular": "Camila Rojas", "numero_cuenta": "110", "saldo_inicial": 20000, "tipo": "ahorro", "tasa_interes": 2.5},  # tasa_interes valida explicita
    {"titular": "Diego Pizarro", "numero_cuenta": "111", "saldo_inicial": 15000, "tipo": "corriente", "limite_giro": 30000},  # limite_giro valido explicito
    {"titular": "  Marta   Soto  ", "numero_cuenta": " 112 ", "saldo_inicial": 8000, "tipo": " Corriente "},  # espacios de sobra en varios campos
    {"titular": "Fernando Vidal", "numero_cuenta": 113, "saldo_inicial": 4000, "tipo": "ahorro", "tasa_interes": -1.5},  # tasa_interes negativa -> default
    {"titular": "Josefa Bravo", "numero_cuenta": 114, "saldo_inicial": 6000, "tipo": "corriente", "limite_giro": -200},  # limite_giro negativo -> default
    {"titular": "Ignacio Toro", "saldo_inicial": 5000, "tipo": "ahorro"},  # sin numero_cuenta -> descartada
    {"numero_cuenta": 115, "saldo_inicial": 3000, "tipo": "corriente"},  # sin titular -> descartada
    {"titular": "Valentina Gomez", "numero_cuenta": 116, "tipo": "ahorro"},  # sin saldo_inicial -> descartada
    {"titular": "Cristobal Nunez", "numero_cuenta": "abc123", "saldo_inicial": 7000, "tipo": "corriente"},  # numero_cuenta con letras -> descartada
    {"titular": "Antonia Reyes", "numero_cuenta": 117, "saldo_inicial": "5500.5", "tipo": "ahorro"},  # saldo con decimales como texto -> ver si falla o pasa

]

resultado = pre_procesar_cuentas(datos_prueba)
print(resultado)

#Parte 2

class Cuenta:
    def __init__(self, titular, numero_cuenta):
        self.titular = titular
        self.numero_cuenta = numero_cuenta
        self.__saldo = 0
        self.tipo_cuenta = ""  # Lo defeiniremos en clases heredadas

    def obtener_informacion_basica(self):
        return f"Titular: {self.titular}, Numero de cuenta: {self.numero_cuenta}"

    def consultar_saldo(self):
        return self.__saldo

    def _modificar_saldo(self, delta):
        self.__saldo = self.__saldo + delta

    def depositar(self, monto):
        if monto <= 0:
            raise ValueError("El monto a depositar debe ser positivo")
        self._modificar_saldo(monto)

    def girar_monto(self, monto):
        if monto <= 0:
            raise ValueError("El monto a girar debe ser positivo")
        if monto > self.__saldo:
            raise ValueError("Saldo insuficiente para realizar el giro")
        self._modificar_saldo(-monto)


class CuentaDeAhorro(Cuenta):
    def __init__(self, titular, numero_cuenta, tasa_interes):
        super().__init__(titular, numero_cuenta)
        self.tasa_interes = tasa_interes
        self.tipo_cuenta = "ahorro"

    def obtener_informacion_basica(self):
        return f"Titular: {self.titular}, Numero de cuenta: {self.numero_cuenta}, Tipo: {self.tipo_cuenta}, Tasa de interes: {self.tasa_interes}%"

    def aplicar_interes(self):
        saldo_actual = self.consultar_saldo()
        interes = saldo_actual * self.tasa_interes / 100
        self.depositar(interes)


class CuentaCorriente(Cuenta):
    def __init__(self, titular, numero_cuenta, limite_giro):
        super().__init__(titular, numero_cuenta)
        self.limite_giro = limite_giro
        self.tipo_cuenta = "corriente"

    def obtener_informacion_basica(self):
        return f"Titular: {self.titular}, Numero de cuenta: {self.numero_cuenta}, Tipo: {self.tipo_cuenta}, Limite de giro: {self.limite_giro}"

    def girar_monto(self, monto):
        if monto <= 0:
            raise ValueError("El monto a girar debe ser positivo")

        saldo_resultante = self.consultar_saldo() - monto

        if saldo_resultante < -self.limite_giro:
            raise ValueError("El giro supera el limite de sobregiro permitido")

        self._modificar_saldo(-monto)


class Banco:
    def __init__(self, nombre):
        self.nombre = nombre
        self.cuentas = []

    def abrir_cuenta(self, cuenta):
        existe = False

        for c in self.cuentas:
            if c.numero_cuenta == cuenta.numero_cuenta:
                existe = True

        if existe:
            print(f"Error: ya existe una cuenta con el numero {cuenta.numero_cuenta}")
        else:
            self.cuentas.append(cuenta)
            print(f"Cuenta {cuenta.numero_cuenta} de {cuenta.titular} abierta correctamente")

    def buscar_cuenta(self, numero_cuenta):
        for cuenta in self.cuentas:
            if cuenta.numero_cuenta == numero_cuenta:
                return cuenta
        print(f"Cuenta {numero_cuenta} no encontrada")

    def transferir(self, numero_origen, numero_destino, monto):
        existe_origen = False
        existe_destino = False
        cuenta_origen = ""
        cuenta_destino = ""

        for cuenta in self.cuentas:
            if cuenta.numero_cuenta == numero_origen:
                existe_origen = True
                cuenta_origen = cuenta
            if cuenta.numero_cuenta == numero_destino:
                existe_destino = True
                cuenta_destino = cuenta

        if existe_origen and existe_destino:
            if monto <= 0:
                print("Error: el monto a transferir debe ser positivo")
            else:
                try:
                    cuenta_origen.girar_monto(monto)
                    cuenta_destino.depositar(monto)
                    print(f"Transferencia de {monto} realizada de la cuenta {numero_origen} a la cuenta {numero_destino}")
                except ValueError as e:
                    print(f"Error al transferir: {e}")
        else:
            print("Error: una o ambas cuentas no existen")

    def mostrar_cuentas(self):
        cuentas_ordenadas = self.cuentas.copy()

        for i in range(len(cuentas_ordenadas)):
            for j in range(len(cuentas_ordenadas) - 1):
                if cuentas_ordenadas[j].numero_cuenta > cuentas_ordenadas[j + 1].numero_cuenta:
                    temporal = cuentas_ordenadas[j]
                    cuentas_ordenadas[j] = cuentas_ordenadas[j + 1]
                    cuentas_ordenadas[j + 1] = temporal

        print(f" --- Cuentas del banco {self.nombre} --- ")
        for cuenta in cuentas_ordenadas:
            print(cuenta.obtener_informacion_basica(), "| Saldo:", cuenta.consultar_saldo())

#puebas para saber si las clases funcionan bien

print(f"{'-'*25} Prueba clase Cuenta {'-'*25}")

cuenta_prueba = Cuenta("Test Usuario", 999)
cuenta_prueba.depositar(1000)
print(cuenta_prueba.consultar_saldo())

cuenta_prueba.girar_monto(300)
print(cuenta_prueba.consultar_saldo())

try:
    cuenta_prueba.girar_monto(5000)
except ValueError as e:
    print(f"Error capturado: {e}")

print(cuenta_prueba.obtener_informacion_basica())


print(f"{'-'*25} Prueba clase CuentaDeAhorro {'-'*25}")

cuenta_ahorro_1 = CuentaDeAhorro("Marta Soto", 200, 2)
cuenta_ahorro_1.depositar(10000)
print(cuenta_ahorro_1.consultar_saldo())

cuenta_ahorro_1.aplicar_interes()
print(cuenta_ahorro_1.consultar_saldo())

print(cuenta_ahorro_1.obtener_informacion_basica())

try:
    cuenta_ahorro_1.girar_monto(50000)
except ValueError as e:
    print(f"Error capturado: {e}")


print(f"{'-'*25} Prueba clase CuentaCorriente {'-'*25}")

cuenta_corriente_1 = CuentaCorriente("Diego Pizarro", 300, 50000)
cuenta_corriente_1.depositar(10000)
print(cuenta_corriente_1.consultar_saldo())

cuenta_corriente_1.girar_monto(30000)
print(cuenta_corriente_1.consultar_saldo())

print(cuenta_corriente_1.obtener_informacion_basica())

try:
    cuenta_corriente_1.girar_monto(40000)
except ValueError as e:
    print(f"Error capturado: {e}")


print(f"{'-'*25} Prueba clase Banco {'-'*25}")

banco = Banco("Banco Estado Ficticio")

cuenta_a = CuentaDeAhorro("Sofia Reyes", 400, 3)
cuenta_b = CuentaCorriente("Matias Leal", 401, 20000)

banco.abrir_cuenta(cuenta_a)
banco.abrir_cuenta(cuenta_b)
banco.abrir_cuenta(cuenta_a)  #fallara numero de cuenta duplicado

cuenta_a.depositar(50000)
cuenta_b.depositar(10000)

banco.mostrar_cuentas()

banco.transferir(400, 401, 20000)
banco.mostrar_cuentas()

banco.transferir(400, 999, 5000)  #fallara cuenta 999 no existe en el banco

banco.buscar_cuenta(999)  #imprimira "no encontrado"

#Unimos nuestra parte 1 y parte 2

print(f"{'='*20} Simulacion del Sistema Bancario {'='*20}")

#Creamos el banco sin las cuentas registradas
banco_simulacion = Banco("Banco Simulacion S.A.")

#A partir de la anterior linea (las dicciones ya limpias)
#creamos los objetos de cuenta correspondientes y los abrimos dentro del banco
for cuenta_datos in resultado:
    if cuenta_datos["tipo"] == "ahorro":
        nueva_cuenta = CuentaDeAhorro(
            cuenta_datos["titular"],
            cuenta_datos["numero_cuenta"],
            cuenta_datos["tasa_interes"]
        )
    else:
        nueva_cuenta = CuentaCorriente(
            cuenta_datos["titular"],
            cuenta_datos["numero_cuenta"],
            cuenta_datos["limite_giro"]
        )

    #depositamos el saldo_inicial
    if cuenta_datos["saldo_inicial"] > 0:
        nueva_cuenta.depositar(cuenta_datos["saldo_inicial"])

    banco_simulacion.abrir_cuenta(nueva_cuenta)

print()
banco_simulacion.mostrar_cuentas()

#aplicamos depositar / girar_monto / aplicar_intereses sobre estas nuevas cuentas

print()
print(f"{'-'*20} Operaciones de la simulacion {'-'*20}")

#Depositamos en la cuenta de; (Ana Maria, numero 101)
cuenta_101 = banco_simulacion.buscar_cuenta(101)
cuenta_101.depositar(2000)
print(f"Deposito realizado. Nuevo saldo cuenta 101: {cuenta_101.consultar_saldo()}")

#Giramos monto de la cuenta corriente de; (Juan Carlos, numero 102)
cuenta_102 = banco_simulacion.buscar_cuenta(102)
cuenta_102.girar_monto(1000)
print(f"Giro realizado. Nuevo saldo cuenta 102: {cuenta_102.consultar_saldo()}")

#Aplicamos el interes a la cuenta de ahorro de; (Ariel Masle, numero 109)
cuenta_109 = banco_simulacion.buscar_cuenta(109)
cuenta_109.aplicar_interes()
print(f"Interes aplicado. Nuevo saldo cuenta 109: {cuenta_109.consultar_saldo()}")

#Transferencia entre dos cuentas (de la 110 a la 111)
banco_simulacion.transferir(110, 111, 5000)

#Consultamos de saldo
cuenta_110 = banco_simulacion.buscar_cuenta(110)
print(f"Saldo final cuenta 110: {cuenta_110.consultar_saldo()}")

#Intento de transferencia invalida ( pq la cuenta no existe)
banco_simulacion.transferir(110, 9999, 1000)

print()
banco_simulacion.mostrar_cuentas()