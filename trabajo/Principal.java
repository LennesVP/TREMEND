
import javax.swing.JOptionPane;


public class Principal {
    public static void main(String[] args) {
        Triangulo triangulito = new Triangulo();
        String texto="";
        triangulito.setLado1(Integer.parseInt(JOptionPane.showInputDialog("Ingrese el primer lado del triangulo"))  );
        triangulito.setLado2(Integer.parseInt(JOptionPane.showInputDialog("Ingrese el segundo lado del triangulo"))  );
        triangulito.setLado3(Integer.parseInt(JOptionPane.showInputDialog("Ingrese el tercer lado del triangulo"))  );
        triangulito.calcularPerimetro();
        Triangulo triangulito2 = new Triangulo();
        triangulito2.setLado1(15);
        triangulito2.setLado2(9);
        triangulito2.setLado3(17);
        triangulito2.calcularPerimetro();
        texto=" el primer perimetro: " + triangulito.getPerimetro()+"\n El segundo´perimetro es "+triangulito2.getPerimetro();
        
        String textoPerimetro="";
        if (triangulito.getPerimetro()>triangulito2.getPerimetro()){
            
            textoPerimetro="El primer triangulo es mayor que el segundo";
        } else if (triangulito.getPerimetro()<triangulito2.getPerimetro()){
            textoPerimetro="El segundo triangulo es mayor que el primero";
        } else {
            textoPerimetro="Los dos triangulos son iguales";
        
        }
        JOptionPane.showMessageDialog(null, texto + "\n" + textoPerimetro.toUpperCase());
    }
}