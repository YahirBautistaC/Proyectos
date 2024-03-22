using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Windows.Forms.DataVisualization.Charting;
using static System.Windows.Forms.VisualStyles.VisualStyleElement;

namespace Calentador_proyecto
{
    public partial class Form1 : Form
    {
        private readonly System.IO.Ports.SerialPort Port = new System.IO.Ports.SerialPort("COM6", 9600) { ReadTimeout = 1000 };
        private bool IsClose;
        private int txtcr, txttp, temp, tiempoRestante, tempFromArduino;
        private readonly object tempLock = new object();
        private int temp1;

        private double temperatura;  // Cambié el tipo de la variable a double
        private double tempEntrada;

        private int intervaloContador = 0;

        private readonly System.Windows.Forms.Timer temporizador = new System.Windows.Forms.Timer { Interval = 1000 };

        public Form1()
        {
            InitializeComponent();

            try
            {
                Port.Open();
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Error al abrir el puerto serial: {ex.Message}", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }

            temporizador.Tick += Temporizador_Tick;
        }

        private void hora_Tick(object sender, EventArgs e) => labelHora.Text = DateTime.Now.ToString("hh:mm:ss");

        private void Temporizador_Tick(object sender, EventArgs e)
        {
            intervaloContador++;
            if (intervaloContador % 10 == 0) // Aquí esta el intervalo de tiempo de cada cuantos segundos agrega datos
            {
                // Agrega el valor actual al gráfico
                AgregarValorAlGrafico();
            }

            if (tiempoRestante > 0)
            {
                tiempoRestante--;
                labelcrono.Text = $"{tiempoRestante}";

                // Llama a VerificarTemperatura cada segundo
                VerificarTemperatura();
            }
            else
            {
                temporizador.Stop();
                MessageBox.Show("Temporizador finalizado.");

                txtcr = txttp = temp = 0;
                Port.Write("A");

                labeltemp.Invoke(new MethodInvoker(() => labeltemp.Text = "0"));

                chart1.Series[0].Points.Clear();
            }
        }

        private void AgregarValorAlGrafico()
        {
            chart1.Series[0].Points.AddXY(tiempoRestante, temperatura);
        }


        // Agrega un método para verificar la temperatura y escribir en el puerto si es necesario
        private void VerificarTemperatura()
        {
            if (temperatura >= tempEntrada)
            {
                Port.Write("A");
            }
            else if (temperatura < tempEntrada)
            {
                Port.Write("E");
            }
        }

        private void EscucharSerial()
        {
            while (!IsClose)
            {
                try
                {
                    string cadena = Port.ReadLine();
                    if (double.TryParse(cadena,out double tempValue))
                    {
                        lock (tempLock)
                        {
                            temperatura = tempValue;
                        }

                        labeltemp.Invoke(new MethodInvoker(delegate
                        {
                            labeltemp.Text = cadena;
                        }));
                    }
                    else
                    {

                    }
                }
                catch (Exception ex)
                {
                    // Puedes manejar el error de manera adecuada, por ejemplo, mostrando un mensaje de error.
                    // MessageBox.Show("Error al leer el puerto serial: " + ex.Message, "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                }
            }
        }

        private void Form1_Load(object sender, EventArgs e) => new Thread(EscucharSerial).Start();

        private void Form1_FormClosed(object sender, FormClosedEventArgs e)
        {
            IsClose = true;
            if (Port.IsOpen)
            {
                // Escribir "A" en el puerto antes de cerrarlo
                Port.Write("A");
                Port.Close();
            }
        }

        private void textcrono_TextChanged(object sender, EventArgs e)
        {
            if (int.TryParse(textcrono.Text, out int valor))
            {
                chart1.Series[0].Points.Clear();
                chart1.ChartAreas[0].AxisY.Minimum = -55;
                chart1.ChartAreas[0].AxisY.Maximum = 125;
                chart1.ChartAreas[0].AxisY.Interval = 15;

                for (int i = 0; i <= valor; i += 15) // Aquí esta el intervalo de eje x
                {
                    chart1.Series[1].Points.AddXY(i, 0);
                }
            }
            else
            {
                MessageBox.Show("Ingrese un valor numérico válido.");
            }
        }

        private void texttemp_TextChanged(object sender, EventArgs e)
        {
            if (double.TryParse(texttemp.Text, out double valorTemp))
            {
                tempEntrada = valorTemp;
            }
            else
            {
                MessageBox.Show("Ingrese un valor numérico válido para la temperatura.");
            }
        }

        private void button2_Click(object sender, EventArgs e)
        {
            try
            {
                txtcr = int.Parse(textcrono.Text);
                txttp = int.Parse(texttemp.Text);

                MessageBox.Show($"Valores guardados: \n{tempEntrada} °C\n{txtcr} seg");
            }
            catch (FormatException ex)
            {
                MessageBox.Show("Error de formato en la entrada. Asegúrate de ingresar números válidos.");
            }
        }

        private void button1_Click(object sender, EventArgs e)
        {
            try
            {
                tiempoRestante = int.Parse(textcrono.Text);
                labelcrono.Text = $"{tiempoRestante}";
                temporizador.Start();
                Port.Write("E");
            }
            catch (FormatException ex)
            {
                MessageBox.Show("Error de formato en la entrada. Asegúrate de ingresar números válidos.");
            }
        }
    }
}