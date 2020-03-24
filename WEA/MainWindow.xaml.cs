using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;
using System.IO;
using LiveCharts;
using LiveCharts.Wpf;


namespace WEA
{
    /// <summary>
    /// MainWindow.xaml에 대한 상호 작용 논리
    /// </summary>
    public partial class MainWindow : Window
    {
        double[] newLength = { 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 2000, 3000, 4000, 5000 };
        double[] Diameter = { 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 2000, 3000, 4000, 5000 };
        double InputDiameter, OutputDiameter, Power, Wavelength, rad, area, q, u, p;
        bool nStart = false;
        private void comboMaterial_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            readCsv(comboMaterial.SelectedIndex + 1);
        }

        private void txtTargetDepth_TextChanged(object sender, TextChangedEventArgs e)
        {
            if (nStart)
            {
                TargetDepth = Convert.ToDouble(txtTargetDepth.Text);
                TargetArea = Convert.ToDouble(txtTargetArea.Text);
                TargetDensity = Convert.ToDouble(txtTargetDensity.Text);
                TargetWeight = TargetDensity * (TargetArea * TargetDepth * 0.1);
                txtTargetWeight.Text = Convert.ToString(TargetWeight);
            }            
        }

        private void txtTargetArea_TextChanged(object sender, TextChangedEventArgs e)
        {
            if (nStart)
            {
                TargetDepth = Convert.ToDouble(txtTargetDepth.Text);
                TargetArea = Convert.ToDouble(txtTargetArea.Text);
                TargetDensity = Convert.ToDouble(txtTargetDensity.Text);
                TargetWeight = TargetDensity * (TargetArea * TargetDepth * 0.1);
                txtTargetWeight.Text = Convert.ToString(TargetWeight);
            }
        }

        private void Button_Click_1(object sender, RoutedEventArgs e)
        {
            TargetWeight = Convert.ToDouble(txtTargetWeight.Text);
            SpecificHeat = Convert.ToDouble(txtSpecificHeat.Text);
            MeltingPoint = Convert.ToDouble(txtMeltingPoint.Text);
            VaporizationPoint = Convert.ToDouble(txtVaporizationPoint.Text);
            MoltenLatentHeat = Convert.ToDouble(txtMoltenLatentHeat.Text);
            VaporizationLatentHeat = Convert.ToDouble(txtVaporizationLatentHeat.Text);
            Temp = Convert.ToDouble(txtTemp.Text);
            Time = Convert.ToDouble(txtTime.Text);
            Loss = Convert.ToDouble(txtLoss.Text);

            double q1 = TargetWeight * SpecificHeat * (MeltingPoint - Temp);
            txtQ1.Text = Convert.ToString((int)q1);
            double q2 = TargetWeight * MoltenLatentHeat;
            txtQ2.Text = Convert.ToString((int)q2);
            double q3 = TargetWeight * SpecificHeat * (VaporizationPoint - Temp) - q1;
            txtQ3.Text = Convert.ToString((int)q3);
            double q4 = TargetWeight * VaporizationLatentHeat;
            txtQ4.Text = Convert.ToString(q4);
            double qTotal = q1 + q2 + q3 + q4;
            txtQtotal.Text = Convert.ToString((int)qTotal);

            double pTotal = qTotal / Time;
            txtPtotal.Text = Convert.ToString((int)pTotal);
            double pNeed = pTotal / (1 - Loss * 0.01);
            txtPneed.Text = Convert.ToString((int)pNeed);
        }

        double TargetDepth, TargetArea, TargetDensity, TargetWeight, SpecificHeat, MeltingPoint, VaporizationPoint, MoltenLatentHeat, VaporizationLatentHeat, Temp, Time, Loss;

        public MainWindow()
        {
            InitializeComponent();

            Values = new ChartValues<double> { 12995, 7540, 5557, 4504, 3841, 3381, 3041, 2778, 2567, 2394, 1543, 1211, 1027, 906 };
            Labels = new[] {"100","200","300","400","500","600","700","800","900","1000","2000","3000","4000","5000" };

            DataContext = this;
        }

        public ChartValues<double> Values { get; set; }
        public string[] Labels { get; set; }

        private void UpdateOnclick(object sender, RoutedEventArgs e)
        {
            InputDiameter = Convert.ToDouble(txtInputDiameter.Text);
            OutputDiameter = Convert.ToDouble(txtOutputDiameter.Text);
            Power = Convert.ToDouble(txtPower.Text);
            Wavelength = Convert.ToDouble(txtWavelength.Text);

            rad = Wavelength / (Math.PI * InputDiameter * 1000000);
            area = Math.Pow(OutputDiameter / 2, 2) * Math.PI;

            for (int i=0; i < 14; i++)
            {
                q = 0.585 * Math.Pow(newLength[i]*0.001, 0.3333);
                u = 3.912 / (newLength[i] *0.001) * Math.Pow(0.55 / 1.064, q);
                p = Power * (area / Math.Pow(rad * newLength[i], 2)) * Math.Pow(Math.E, -u * newLength[i] * 0.001) * newLength[i] * 0.001;
                Diameter[i] = 2.44 * Wavelength * 0.0000001 * newLength[i] / OutputDiameter;
                Values[i] = (int)p;
            }
            updateDiameter();
            Chart.Update(true);
        }

        private void Window_Loaded(object sender, RoutedEventArgs e)
        {
            txtDate.Text = System.DateTime.Now.ToLongDateString();

            var rows = File.ReadAllLines("variable.csv").Select(l => l.Split(',').ToArray()).ToArray();
            for (int i = 1; i < rows.Length; i++)
            {
                comboMaterial.Items.Add(Convert.ToString(rows[i][0]));
            }
            comboMaterial.SelectedItem = Convert.ToString(rows[1][0]);
            readCsv(1);

            nStart = true;
        }

        private void updateDiameter()
        {
            txtDiameter100.Text = Convert.ToString(Diameter[0]);
            txtDiameter200.Text = Convert.ToString(Diameter[1]);
            txtDiameter300.Text = Convert.ToString(Diameter[2]);
            txtDiameter400.Text = Convert.ToString(Diameter[3]);
            txtDiameter500.Text = Convert.ToString(Diameter[4]);
            txtDiameter600.Text = Convert.ToString(Diameter[5]);
            txtDiameter700.Text = Convert.ToString(Diameter[6]);
            txtDiameter800.Text = Convert.ToString(Diameter[7]);
            txtDiameter900.Text = Convert.ToString(Diameter[8]);
            txtDiameter1000.Text = Convert.ToString(Diameter[9]);
            txtDiameter2000.Text = Convert.ToString(Diameter[10]);
            txtDiameter3000.Text = Convert.ToString(Diameter[11]);
            txtDiameter4000.Text = Convert.ToString(Diameter[12]);
            txtDiameter5000.Text = Convert.ToString(Diameter[13]);
        }

        private void readCsv(int d)
        {
            var rows = File.ReadAllLines("variable.csv").Select(l => l.Split(',').ToArray()).ToArray();

            txtTargetDensity.Text = Convert.ToString(rows[d][1]);
            txtSpecificHeat.Text = Convert.ToString(rows[d][2]);
            txtMeltingPoint.Text = Convert.ToString(rows[d][3]);
            txtVaporizationPoint.Text = Convert.ToString(rows[d][4]);
            txtMoltenLatentHeat.Text = Convert.ToString(rows[d][5]);
            txtVaporizationLatentHeat.Text = Convert.ToString(rows[d][6]);
        }
    }
}
