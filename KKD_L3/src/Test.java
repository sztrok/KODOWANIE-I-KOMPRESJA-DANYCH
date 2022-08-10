import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.util.*;

public class Test {

    public static List<Integer> encode(String text){
        int dictSize = 256;
        Map<String, Integer> dictionary = new HashMap<>();
        for(int i=0; i<dictSize; i++){
            dictionary.put(String.valueOf((char) i),i);

        }
        String foundChars="";
        List<Integer> result = new ArrayList<>();
        for(char c: text.toCharArray()){

            String newStringToDict = foundChars+c;

            if(dictionary.containsKey(newStringToDict)){
                foundChars=newStringToDict;

            }
            else{

                result.add(dictionary.get(foundChars));
                dictionary.put(newStringToDict,dictSize++);
                foundChars=String.valueOf(c);
            }
        }
        if(!foundChars.isEmpty()){
            result.add(dictionary.get(foundChars));
        }

        return result;

    }

    public static String decode(List<Integer> encodedText){
        int dictSize = 256;
        Map<Integer,String> dictionary = new HashMap<>();
        for(int i=0; i<dictSize; i++){
            dictionary.put(i, String.valueOf((char)i));
        }

        String chars = String.valueOf((char)encodedText.remove(0).intValue());
        StringBuilder result = new StringBuilder(chars);

        for(int code: encodedText){
            String entry = dictionary.containsKey(code) ? dictionary.get(code) : chars + chars.charAt(0);
            result.append(entry);
            dictionary.put(dictSize++, chars+entry.charAt(0));
            chars = entry;
        }

        return result.toString();
    }

    public static void main(String[] args) throws IOException {
//        File file = new File(".//src//test1.bin");
//        File file = new File(".//src//test2.bin");
//        File file = new File(".//src//test3.bin");
        File file = new File(".//src//pan-tadeusz-czyli-ostatni-zajazd-na-litwie.txt");
        byte[] fileContent = Files.readAllBytes(file.toPath());
        String test = new String(fileContent);
        int[] charFreqs = new int[65534];
        int summ = 0;
        for (char c : test.toCharArray()) {
            charFreqs[c]++;
            summ++;
        }

        double baseEntropy = entropy(charFreqs,summ);



        List<Integer> comp = encode(test);
//        System.out.println(comp);
//        System.out.println(decode(comp));
        String result = "";
        comp.removeIf(Objects::isNull);
//        if(comp.contains(null)){
//            int index = comp.indexOf(null);
//            comp.set(index, 0);
//        }



        for (Integer integer : comp) {
            if (integer <= 255) {
                String string = Integer.toBinaryString(integer);
                String padding = String.format("%8s", string).replaceAll(" ", "0");
                result += padding;
            } else {
                result += Integer.toBinaryString(integer);
            }
        }

        System.out.println("SUMM: "+summ);
        System.out.println("ENTROPY: "+baseEntropy);
        System.out.println("NORMAL LENGTH: "+summ*8);
        System.out.println("ENCODED LENGTH: "+result.length());
        double compressionRate = 1-((double) result.length() / (double)(summ*8));
        System.out.println("COMPRESSION RATE: "+compressionRate);
//        System.out.println(Integer.toBinaryString(32));
    }

    public static double entropy(int[] alphabet, int summ){
        if(summ==0) return -1d;
        double res = 0d;
        for (int j : alphabet) {
            if (j != 0) {
                double value = j * 1d;
                res += value * Math.log(value);
            }
        }
        return Math.log(summ)-res/summ;
    }
}
