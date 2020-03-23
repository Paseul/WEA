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
        public const double E = 2.7182818284590451;
        double rad = 1.064 / (Math.PI * 50 * 1000);
        double area = Math.Pow(0.02/2, 2)*Math.PI;
        public MainWindow()
        {
            InitializeComponent();

            Values = new ChartValues<double> { 15000, 375, 420, 500, 160, 140, 150, 375, 420, 500, 160, 140, 160, 140 };
            Labels = new[] {"100","200","300","400","500","600","700","800","900","1000","2000","3000","4000","5000" };
            DataContext = this;
        }

        public ChartValues<double> Values { get; set; }
        public string[] Labels { get; set; }

        private void UpdateOnclick(object sender, RoutedEventArgs e)
        {
            double[] newValues = { 12995, 7540, 5557, 4504, 3841, 3381, 3041, 2778, 2567, 2394, 1543, 1211, 1027, 906 };
            for(int i=0; i < 14; i++)
            {
                double q = 0.585 * Math.Pow(newLength[i]*0.001, 0.33);
                double u = 3.912 / (newLength[i] *0.001) * Math.Pow(0.55 / 1.064, q);
                double p = 5000 * (area / Math.Pow(rad * newLength[i], 2)) * Math.Pow(Math.E, -u * newLength[i] * 0.001) * newLength[i] * 0.001;

                Values[i] = p;

            }

            Chart.Update(true);
        }
    }
}
