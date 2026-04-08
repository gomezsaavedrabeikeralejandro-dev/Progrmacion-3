import tkinter as tk
import random
import time

class Carrera:
    def __init__(self, root):
        self.root = root
        self.root.title("🏁 Simulador de Carrera")

        self.canvas = tk.Canvas(root, width=900, height=450, bg="lightgray")
        self.canvas.pack()

       
        self.meta_derecha = 850
        self.meta_izquierda = 10

        
        for y in range(0, 450, 20):
            color = "black" if (y // 20) % 2 == 0 else "white"
            self.canvas.create_rectangle(self.meta_derecha - 10, y, self.meta_derecha, y + 20, fill=color, outline="")

        
        for y in range(0, 450, 20):
            color = "black" if (y // 20) % 2 == 0 else "white"
            self.canvas.create_rectangle(self.meta_izquierda, y, self.meta_izquierda + 10, y + 20, fill=color, outline="")

        self.vehiculos = []
        self.velocidades = []
        self.direccion = []
        self.vueltas = []
        self.tiempos = {}

        
        frame = tk.Frame(root)
        frame.pack(pady=10)

        tk.Label(frame, text="Apuesta (1-10):").grid(row=0, column=0)
        self.apuesta = tk.Entry(frame, width=5)
        self.apuesta.grid(row=0, column=1)

        tk.Label(frame, text="Rondas:").grid(row=0, column=2)
        self.rondas_entry = tk.Entry(frame, width=5)
        self.rondas_entry.grid(row=0, column=3)

        tk.Label(frame, text="Velocidad global:").grid(row=0, column=4)
        self.slider = tk.Scale(frame, from_=1, to=10, orient="horizontal")
        self.slider.set(5)
        self.slider.grid(row=0, column=5)

        tk.Button(frame, text="Iniciar Carrera", command=self.iniciar).grid(row=0, column=6)

       
        for i in range(10):
            y = 30 + i * 40
            vehiculo = self.canvas.create_rectangle(10, y, 60, y + 25, fill=self.random_color())

            self.vehiculos.append(vehiculo)
            self.velocidades.append(random.randint(2, 6))
            self.direccion.append(1)
            self.vueltas.append(0)

    def random_color(self):
        return f"#{random.randint(0,255):02x}{random.randint(0,255):02x}{random.randint(0,255):02x}"

    def iniciar(self):
        self.tiempos = {}
        self.rondas = int(self.rondas_entry.get() or 1)
        self.apuesta_usuario = int(self.apuesta.get() or 1)

        
        for i, v in enumerate(self.vehiculos):
            y = 30 + i * 40
            self.canvas.coords(v, 10, y, 60, y + 25)
            self.direccion[i] = 1
            self.vueltas[i] = 0

        self.inicio_tiempo = time.time()
        self.mover()

    def mover(self):
        terminados = 0

        for i, v in enumerate(self.vehiculos):
            coords = self.canvas.coords(v)

            if i not in self.tiempos:

                velocidad = self.velocidades[i] * (self.slider.get() / 5)

             
                if self.direccion[i] == 1:
                    self.canvas.move(v, velocidad, 0)
                else:
                    self.canvas.move(v, -velocidad, 0)

                coords = self.canvas.coords(v)

                
                if coords[2] >= self.meta_derecha:
                    self.direccion[i] = -1

               
                if coords[0] <= self.meta_izquierda:
                    self.direccion[i] = 1
                    self.vueltas[i] += 1

              
                if self.vueltas[i] >= self.rondas:
                    self.tiempos[i] = time.time() - self.inicio_tiempo

            else:
                terminados += 1

        if terminados < 10:
            self.root.after(40, self.mover)
        else:
            self.resultados()

    def resultados(self):
        ranking = sorted(self.tiempos.items(), key=lambda x: x[1])

        ventana = tk.Toplevel(self.root)
        ventana.title("🏆 Resultados")

        tk.Label(ventana, text="RESULTADOS FINALES", font=("Arial", 14, "bold")).pack(pady=10)

        for pos, (vehiculo, tiempo) in enumerate(ranking, start=1):
            texto = f"{pos}. Vehículo {vehiculo+1} - {tiempo:.2f} segundos"
            tk.Label(ventana, text=texto).pack()

        ganador = ranking[0][0] + 1

        if ganador == self.apuesta_usuario:
            resultado = "🎉 ¡Ganaste la apuesta!"
        else:
            resultado = f"❌ Perdiste. Ganó el vehículo {ganador}"

        tk.Label(ventana, text=resultado, fg="red", font=("Arial", 12)).pack(pady=10)



root = tk.Tk()
app = Carrera(root)
root.mainloop()