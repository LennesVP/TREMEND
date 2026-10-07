public class Triangulo {
 
    private int lado1;
    private int lado2;
    private int lado3;
    private int perimetro;
    private double area;
 
    public Triangulo() {
        this.lado1 = 0;
        this.lado2 = 0;
        this.lado3 = 0;
        this.perimetro = 0;
        this.area = 0;
    }
 
    public void setLado1(int lado1) {
        this.lado1 = lado1;
    }
 
    public void setLado2(int lado2) {
        this.lado2 = lado2;
    }
 
    public void setLado3(int lado3) {
        this.lado3 = lado3;
    }
 
    public int getPerimetro() {
        return perimetro;
    }
 
    public double getArea() {
        return area;
    }
 
    public void calcularPerimetro() {
        perimetro = lado1 + lado2 + lado3;
    }
}