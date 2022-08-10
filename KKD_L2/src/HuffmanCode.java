import java.io.File;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.util.Arrays;
import java.util.PriorityQueue;

abstract class HuffmanTree implements Comparable<HuffmanTree> {
    public final int frequency;
    public HuffmanTree(int freq) { frequency = freq; }

    public int compareTo(HuffmanTree tree) {
        return frequency - tree.frequency;
    }
}

class HuffmanLeaf extends HuffmanTree {
    public final char value;

    public HuffmanLeaf(int freq, char val) {
        super(freq);
        value = val;
    }
}

class HuffmanNode extends HuffmanTree {
    public final HuffmanTree left, right;

    public HuffmanNode(HuffmanTree l, HuffmanTree r) {
        super(l.frequency + r.frequency);
        left = l;
        right = r;
    }
}

public class HuffmanCode {

    static int encodedLength =0;

    public static HuffmanTree buildTree(int[] charFreqs) {
        PriorityQueue<HuffmanTree> trees = new PriorityQueue<>();

        for (int i = 0; i < charFreqs.length; i++)
            if (charFreqs[i] > 0)
                trees.offer(new HuffmanLeaf(charFreqs[i], (char)i));

        assert trees.size() > 0;

        while (trees.size() > 1) {

            HuffmanTree a = trees.poll();
            HuffmanTree b = trees.poll();

            trees.offer(new HuffmanNode(a, b));
        }
        return trees.poll();
    }

    public static void printCodes(HuffmanTree tree, StringBuffer prefix) {
        assert tree != null;
        if (tree instanceof HuffmanLeaf) {
            HuffmanLeaf leaf = (HuffmanLeaf)tree;

            encodedLength += leaf.frequency*prefix.length();

            System.out.println(leaf.value + "\t" + leaf.frequency + "\t" + prefix );


        } else if (tree instanceof HuffmanNode) {
            HuffmanNode node = (HuffmanNode)tree;

            prefix.append('0');
            printCodes(node.left, prefix);
            prefix.deleteCharAt(prefix.length()-1);

            prefix.append('1');
            printCodes(node.right, prefix);
            prefix.deleteCharAt(prefix.length()-1);
        }
    }

    public static void main(String[] args) throws IOException {
        File file = new File(".//src//pan-tadeusz-czyli-ostatni-zajazd-na-litwie.txt");
//        File file = new File(".//src//test1.bin");
//        File file = new File(".//src//test2.bin");
//        File file = new File(".//src//test3.bin");
        byte[] fileContent = Files.readAllBytes(file.toPath());

        String test = new String(fileContent);
        int[] charFreqs = new int[65534];
        int summ = 0;
        for (char c : test.toCharArray()) {
            charFreqs[c]++;
            summ++;
        }
        HuffmanTree tree = buildTree(charFreqs);
        double entropy = entropy(charFreqs,summ);


        printCodes(tree, new StringBuffer());
        System.out.println("SUMM: "+summ);
        System.out.println("ENTROPY: "+entropy);
        System.out.println("NORMAL LENGTH: "+summ*8);
        System.out.println("ENCODED LENGTH: "+encodedLength);
        double compressionRate = 1-((double) encodedLength/(double)(summ*8));
        System.out.println("COMPRESSION RATE: "+compressionRate);
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