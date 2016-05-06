package validation;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.Arrays;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Scanner;

public class Test1 {
	public static void main(String[] args) throws FileNotFoundException {
		Scanner scanner = null;
		Map<Integer, HashSet<Long>> positive = new HashMap<>();
		scanner = new Scanner(new File("regions"), "latin1");

		while (scanner != null && scanner.hasNextLine()) {
			String line = scanner.nextLine();
			String[] tmp = line.split(":");

			// int chNo = Integer.parseInt(tmp[0]);
			if (tmp[3].equals("1 ") && tmp[0].matches("[1-9]|10")) {
				// if (tmp[0].matches("[1-9]|10")) {
				Integer chNo = Integer.parseInt(tmp[0]);
				// System.out.println(tmp[0]);
				if (!positive.containsKey(chNo)) {
					positive.put(chNo, new HashSet<Long>());
				}
				// System.out.println(tmp[2]);
				Long end = Long.parseLong(tmp[2]);
				positive.get(chNo).add(end);
			}
		}
		scanner.close();
		// System.out.println(positive.get(1).size());

		scanner = null;
		/**
		 * change you testfile name here
		 */
		HashSet<Long> predict = new HashSet<>();
		scanner = new Scanner(new File("salt_TTS_9_result.csv"), "latin1");
		scanner.nextLine();
		int all = 0;
		int dif30 = 0;
		int dif50 = 0;
		int dif100 = 0;
		int dif200 = 0;
		int dif500 = 0;
		int dif1000 = 0;
		while (scanner != null && scanner.hasNextLine()) {
			String line = scanner.nextLine();
			String[] tmp = line.split(",");
			System.out.println(Arrays.toString(tmp));
			int chNo = Integer.parseInt(tmp[0]);
			Long pred = Long.parseLong(tmp[1]);
			predict.add(pred);
			//if (pred < 52000000 && pred>45000000) {
			if (true) {
				all++;
				// System.out.println(tmp[1]);
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
		}
		scanner.close();
		System.out.println("----------");
		System.out.println("All TTS we predict: " + all);
		System.out.println("Match with true TTS: ");
		System.out.println("dif<30: " + dif30 + " ratio: " + (double) dif30 / all);
		System.out.println();
		System.out.println("dif<50: " + dif50 + " ratio: " + (double) dif50 / all);
		dif50+=dif30;
		System.out.println("dif<50 accumulate: " + dif50 + " ratio: " + (double) dif50 / all);
		System.out.println();
		System.out.println("dif<100: " + dif100 + " ratio: " + (double) dif100 / all);
		dif100+=dif50;
		System.out.println("dif<100 accumulate: " + dif100 + " ratio: " + (double) dif100 / all);
		System.out.println();
		System.out.println("dif<200: " + dif200 + " ratio: " + (double) dif200 / all);
		dif200+=dif100;
		System.out.println("dif<200 accumulate: " + dif200 + " ratio: " + (double) dif200 / all);
		System.out.println();
		System.out.println("dif<500: " + dif500 + " ratio: " + (double) dif500 / all);
		dif500+=dif200;
		System.out.println("dif<500 accumulate: " + dif500 + " ratio: " + (double) dif500 / all);
		System.out.println();
		System.out.println("dif<1000: " + dif1000 + " ratio: " + (double) dif1000 / all);
		dif1000+=dif500;
		System.out.println("dif<1000 accumulate: " + dif1000 + " ratio: " + (double) dif1000 / all);
		System.out.println("----------");
		
		all = 0;
		dif30 = 0;
		dif50 = 0;
		dif100 = 0;
		dif200 = 0;
		int dif400=0;
		dif500 = 0;
		int dif600=0;
		int dif800=0;
		dif1000 = 0;
		
		for(Long end : positive.get(9)){
			if(end < 52000000) {
				all++;
				for(Long pred : predict){
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
					if (Math.abs(pred - end) <= 400) {
						dif400++;
						break;
					}
					if (Math.abs(pred - end) <= 500) {
						dif500++;
						break;
					}
					if (Math.abs(pred - end) <= 600) {
						dif600++;
						break;
					}
					if (Math.abs(pred - end) <= 800) {
						dif800++;
						break;
					}
					if (Math.abs(pred - end) <= 1000) {
						dif1000++;
						break;
					}
				}
			}
		}
		
		System.out.println("All true positive in this region: " + all);
		System.out.println("Numbers of being found in prediction: ");
		System.out.println("dif<30: " + dif30 + " ratio: " + (double) dif30 / all);
		dif50+=dif30;
		System.out.println("dif<50: " + dif50 + " ratio: " + (double) dif30 / all);
		dif100+=dif50;
		System.out.println("dif<100: " + dif100 + " ratio: " + (double) dif100 / all);
		dif200+=dif100;
		System.out.println("dif<200: " + dif200 + " ratio: " + (double) dif200 / all);
		dif400+=dif200;
		System.out.println("dif<400: " + dif400 + " ratio: " + (double) dif400 / all);
		dif500+=dif400;
		System.out.println("dif<500: " + dif500 + " ratio: " + (double) dif500 / all);
		dif600+=dif500;
		System.out.println("dif<600: " + dif600 + " ratio: " + (double) dif600 / all);
		dif800+=dif600;
		System.out.println("dif<800: " + dif800 + " ratio: " + (double) dif800 / all);
		dif1000+=dif800;
		System.out.println("dif<1000: " + dif1000 + " ratio: " + (double) dif1000 / all);
		System.out.println("----------");
	}
}
