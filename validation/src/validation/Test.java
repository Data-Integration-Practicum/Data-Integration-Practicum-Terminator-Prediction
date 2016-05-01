package validation;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Scanner;

public class Test {
	public static void main(String[] args) throws FileNotFoundException {
		Scanner scanner = null;
		Map<Integer, HashSet<Long>> positive = new HashMap<>();
		scanner = new Scanner(new File("regions"), "latin1");
		while (scanner != null && scanner.hasNextLine()) {
			String line = scanner.nextLine();
			String[] tmp = line.split(":");
			// System.out.println(tmp[3]);
			// int chNo = Integer.parseInt(tmp[0]);
			if (tmp[3].equals("1 ") && tmp[0].matches("[1-9]|10")) {
				int chNo = Integer.parseInt(tmp[0]);
				// System.out.println(tmp[0]);
				if (!positive.containsKey(tmp[0])) {
					positive.put(chNo, new HashSet<Long>());
				}
				// System.out.println(tmp[2]);
				Long end = Long.parseLong(tmp[2]);
				positive.get(tmp[0]).add(end);
			}
		}
		scanner.close();
		System.out.println(positive.get(1).size());

		scanner = null;
		scanner = new Scanner(new File("output"), "latin1");
		int all = 0;
		int dif30 = 0;
		int dif50 = 0;
		int dif100 = 0;
		int dif200 = 0;
		int dif500 = 0;
		int dif1000 = 0;
		while (scanner != null && scanner.hasNextLine()) {
			String line = scanner.nextLine();
			all++;
			String[] tmp = line.split(",");
			int chNo = Integer.parseInt(tmp[0]);
			Long pred = Long.parseLong(tmp[1]);
			HashSet<Long> curr = positive.get(chNo);
			for (Long end : curr) {
				if (Math.abs(pred - end) <= 30) {
					dif30++;
					break;
				}
				if (Math.abs(pred - end) <= 50) {
					dif50++;
					break;
				}
				if (Math.abs(pred - end) <= 100) {
					dif100++;
					break;
				}
				if (Math.abs(pred - end) <= 200) {
					dif200++;
					break;
				}
				if (Math.abs(pred - end) <= 500) {
					dif500++;
					break;
				}
				if (Math.abs(pred - end) <= 1000) {
					dif1000++;
					break;
				}
			}
		}
		scanner.close();
		System.out.println("all: " + all);
		System.out.println("dif30: " + dif30 + " ratio: " + (double)dif30/all);
		System.out.println("dif50: " + dif50 + " ratio: " + (double)dif50/all);
		System.out.println("dif100: " + dif100 + " ratio: " + (double)dif100/all);
		System.out.println("dif200: " + dif200 + " ratio: " + (double)dif200/all);
		System.out.println("dif500: " + dif500 + " ratio: " + (double)dif500/all);
		System.out.println("dif1000: " + dif1000 + " ratio: " + (double)dif1000/all);
	}
}
