import os
import subprocess
import shutil
from grade import GRADING_DIR
import re
global path
path = ""

def log(comment: str) -> None:
    p = os.path.join(path, f"test.log")
    with open(path, 'a') as f:
        f.write(f"{comment} \n") 
        f.close()

def copy() -> bool:
    try:
        # Copy Necessary Files
        shutil.copytree(GRADING_DIR, path, dirs_exist_ok=True)
        return True
    except Exception as e:
        print(f"Error copying files: {e}")
        return False

def compile():
    # gcc -Wall -std=c99 -D_XOPEN_SOURCE=500 -g sequence.c -o sequence
    compile_cmd = ['gcc', '-Wall', '-std=c99', '-D_XOPEN_SOURCE=500', '-g', 'sequence.c', '-o', 'sequence']
    try:
        result = subprocess.run(compile_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=path)
        return result
    except Exception as e:
        print(f"Compilation error: {e.stderr.decode('utf-8')}")
        return False

def test1() -> int:
    # First, try one worker on one of the small input files. (3 pts)
    # ./sequence 0 1 < input-1.txt 
    # Total count: 2
    score: int = 0
    try:
        test_cmd = ['./sequence', '0', '1', '<', 'input-1.txt']
        result = subprocess.run(test_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=path)
        if result.returncode == 0:
            output = result.stdout.decode('utf-8').strip()
            if output == "Total count: 2":
                score += 3
                log("Test Case 1 Passed")
            else:
                log(f"Test Case 1 Failed: Expected 'Total count: 2', got '{output}'")
        else:
            log(f"Test Case 1 Failed: {result.stderr.decode('utf-8')}")
        return score
    except Exception as e:
        print(f"Test Case 1 Error: {e}")
        log(f"Test Case 1 Error: {e}")
        return score


def test2() -> int:
    # Then, try two workers on a larger input file. (3 pts)

    # ./sequence 30 2 < input-3.txt 
    # Total count: 9
    score: int = 0
    try:
        test_cmd = ['./sequence', '30', '2', '<', 'input-3.txt']
        result = subprocess.run(test_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=path)
        if result.returncode == 0:
            output = result.stdout.decode('utf-8').strip()
            if output == "Total count: 9":
                score += 3
                log("Test Case 2 Passed")
            else:
                log(f"Test Case 2 Failed: Expected 'Total count: 9', got '{output}'")
        else:
            log(f"Test Case 2 Failed: {result.stderr.decode('utf-8')}")
        return score
    except Exception as e:
        print(f"Test Case 2 Error: {e}")
        log(f"Test Case 2 Error: {e}")
        return score

def test3_check(output: str) -> bool:
    # Regular expression pattern to capture process ID, local count, and sequence
    pattern = r"I'm process (\d+)\. Local count: (\d+)\. Sequence found at: (\d+-\d+)\."
    matches = re.findall(pattern, output)
    
    sequences = ['14-35', '14-36', '14-37', '16-33', '18-30', '18-32', '13-30', '13-32', '15-31']
    process_ids = set()
    # Display the results
    for match in matches:
        process_id, local_count, sequence = match
        process_ids.add(process_id)
        if sequence not in sequences:
            return False
        sequences.remove(sequence)
    
    if len(process_ids) != 2:
        return False
    if len(sequences) != 0:
        return False
    
    total_count_pattern = r"Total count: (\d+)"
    total_count_match = re.search(total_count_pattern, output)
    total_count = int(total_count_match.group(1)) if total_count_match else 0
    if total_count != 9:
        return False
    return True
        
        

def test3() -> int:
    # See if they got the report feature using 2 workers. They can
    # report them in any order with different pids and local 
    # counts from the sample run below. But each subsequence found should be the same. The local 
    # counts might be different from our solution, 
    # but the global count should be the same.(3 pts)

    # ./sequence 30 2 report < input-3.txt 
    # I'm process 1282713. Local count: 1. Sequence found at: 14-35.
    # I'm process 1282713. Local count: 2. Sequence found at: 14-36.
    # I'm process 1282713. Local count: 3. Sequence found at: 14-37.
    # I'm process 1282713. Local count: 4. Sequence found at: 16-33.
    # I'm process 1282713. Local count: 5. Sequence found at: 18-30.
    # I'm process 1282713. Local count: 6. Sequence found at: 18-32.
    # I'm process 1282714. Local count: 1. Sequence found at: 13-30.
    # I'm process 1282714. Local count: 2. Sequence found at: 13-32.
    # I'm process 1282714. Local count: 3. Sequence found at: 15-31.
    # Total count: 9 
    score: int = 0
    try:
        test_cmd = ['./sequence', '30', '2','report', '<', 'input-3.txt']
        result = subprocess.run(test_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=path)
        if result.returncode == 0:
            output = result.stdout.decode('utf-8').strip()
            if test3_check(output):
                score += 3
                log("Test Case 3 Passed")
            else:
                log(f"Test Case 3 Failed: Expected 'Total count: 9', got '{output}'")
        else:
            log(f"Test Case 3 Failed: {result.stderr.decode('utf-8')}")
        return score
    except Exception as e:
        print(f"Test Case 3 Error: {e}")
        log(f"Test Case 3 Error: {e}")
        return score

def test4_check(output: str) -> bool:
    # Regular expression pattern to capture process ID, local count, and sequence
    pattern = r"I'm process (\d+)\. Local count: (\d+)\. Sequence found at: (\d+-\d+)\."
    matches = re.findall(pattern, output)
    
    sequences = ['53361-64855', '53361-64856', '53364-64852', '53374-64850', '53358-64849']
    process_ids = set()
    # Display the results
    for match in matches:
        process_id, local_count, sequence = match
        process_ids.add(process_id)
        if sequence not in sequences:
            return False
        sequences.remove(sequence)
    
    if len(process_ids) != 7:
        return False
    if len(sequences) != 0:
        return False
    
    total_count_pattern = r"Total count: (\d+)"
    total_count_match = re.search(total_count_pattern, output)
    total_count = int(total_count_match.group(1)) if total_count_match else 0
    if total_count!= 5:
        return False
    return True

def test4() -> int:
    # Try the same input with a number of workers that doesn't evenly
    # divide the number of inputs (3 pts)

    # ./sequence 1345 7 report < input-4.txt 
    # I'm process 1285168. Local count: 1. Sequence found at: 53361-64855.
    # I'm process 1285168. Local count: 2. Sequence found at: 53361-64856.
    # I'm process 1285171. Local count: 1. Sequence found at: 53364-64852.
    # I'm process 1285174. Local count: 1. Sequence found at: 53374-64850.
    # I'm process 1285169. Local count: 0.
    # I'm process 1285170. Local count: 0.
    # I'm process 1285172. Local count: 1. Sequence found at: 53358-64849.
    # I'm process 1285173. Local count: 0.
    # Total count: 5
    score: int = 0
    try:
        test_cmd = ['./sequence', '1345', '7','report', '<', 'input-4.txt']
        result = subprocess.run(test_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=path)
        if result.returncode == 0:
            output = result.stdout.decode('utf-8').strip()
            if test4_check(output):
                score += 3
                log("Test Case 4 Passed")
            else:
                log(f"Test Case 4 Failed: Expected 'Total count: 5', got '{output}'")
        else:
            log(f"Test Case 4 Failed: {result.stderr.decode('utf-8')}")
        return score
    except Exception as e:
        print(f"Test Case 4 Error: {e}")
        log(f"Test Case 4 Error: {e}")
        return score

def test5_check(output: str) -> bool:
    # Regular expression pattern to capture process ID, local count, and sequence
    pattern = r"I'm process (\d+)\. Local count: (\d+)\. Sequence found at: (\d+-\d+)\."
    matches = re.findall(pattern, output)
    
    sequences = ['53361-64855', '53361-64856', '53358-64849', '53374-64850', '53364-64852']
    process_ids = set()
    # Display the results
    for match in matches:
        process_id, local_count, sequence = match
        process_ids.add(process_id)
        if sequence not in sequences:
            return False
        sequences.remove(sequence)
    
    if len(process_ids)!= 4:
        return False
    if len(sequences) != 0:
        return False
    
    total_count_pattern = r"Total count: (\d+)"
    total_count_match = re.search(total_count_pattern, output)
    total_count = int(total_count_match.group(1)) if total_count_match else 0
    if total_count!= 5:
        return False
    return True


def test5() -> int:
    # Try their solution on the largest test case we gave them with
    # the assignment, using four workers (3 pts)

    # ./sequence 1345 4 report < input-4.txt 
    # I'm process 1285151. Local count: 1. Sequence found at: 53361-64855.
    # I'm process 1285151. Local count: 2. Sequence found at: 53361-64856.
    # I'm process 1285152. Local count: 1. Sequence found at: 53358-64849.
    # I'm process 1285152. Local count: 2. Sequence found at: 53374-64850.
    # I'm process 1285150. Local count: 1. Sequence found at: 53364-64852.
    # I'm process 1285153. Local count: 0.
    # Total count: 5
    score: int = 0
    try:
        test_cmd = ['./sequence', '1345', '4','report', '<', 'input-4.txt']
        result = subprocess.run(test_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=path)
        if result.returncode == 0:
            output = result.stdout.decode('utf-8').strip()
            if test5_check(output):
                score += 3
                log("Test Case 5 Passed")
            else:
                log(f"Test Case 5 Failed: Expected 'Total count: 5', got '{output}'")
        else:
            log(f"Test Case 5 Failed: {result.stderr.decode('utf-8')}")
        return score
    except Exception as e:
        print(f"Test Case 5 Error: {e}")
        log(f"Test Case 5 Error: {e}")
        return score

def test6() -> int:
    
    # # Then, we'll test to make sure they get performance improvement with
    # # multiple workers. This is worth 12 points. These tests will take
    # # some time, so you will probably want to automate them and then check
    # # the results later.

    # # First, run their solution with 1 worker on test input 6. We didn't
    # # give them this test input. It contains 120,000 values.
    # # Note how much real runtime it takes. This could take a while,
    # # depending on how they implemented their solution. I'd give it a
    # # time limit of at most 3 minutes. You can see my solution finishes
    # # in about 19.5 seconds, but their runtimes will be different and will
    # # vary some from execution to execution.

    # # Make sure they got the right result: (5 pts)

    # time ./sequence 100 1 < input-5.txt 
    # Total count: 2735249

    # real	0m19.461s
    # user	0m19.364s
    # sys	0m0.002s

    # # Then, try the same test file with more workers. If you have a
    # # 4-core system, it should be almost 4 times as fast as measured in
    # # real time.
    # # Charge up to 12 points if they don't get speedup. My solution runs
    # # around 3.9 times to 4 times faster with 4 workers (on a 4-core
    # # system). So, I'd say they should run at least 3 times as fast with
    # # 4 workers as they do with just one worker. You can charge between
    # # -4 and -12 points if they don't get this much speedup.

    # time ./sequence 100 4 < input-5.txt 
    # Total count: 2735249

    # real	0m4.824s
    # user	0m19.038s
    # sys	0m0.008s

    #   Be sure to tell students what tests they failed on and something
    #   about what went wrong. Keep in mind, they didn't get input-5.txt
    #   with the assignment, so you'll need to say that this is an extra
    #   test we added (a sequence of 120,000 values). For example:

    #   -3 Your program didn't give the right output when I ran it with a
    #    number of workers that didn't evenly divide the number of points
    #    in the list.

    #   or

    #   -12 Your program gave the right output on all our test cases, but you
    #    didn't get any speedup with multiple workers. We tried this on
    #    on a new test input with 120,000 values.
    score: int = 0
    try:
        # get execution time for time ./sequence 100 1 < input-5.txt and log
        test_cmd = ['time', './sequence', '100', '1', '<', 'input-5.txt']
        result = subprocess.run(test_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=path)
        if result.returncode == 0:
            output = result.stdout.decode('utf-8').strip()
            # only get last 10 lines of output
            output = output.split('\n')[-10:]
            log("Test Case 6 (1)")
            log(output)
        else:
            log(f"Test Case 6 (1)Failed: {result.stderr.decode('utf-8')}")
            return score
        
        # get execution time for time ./sequence 100 4 < input-5.txt and log
        test_cmd = ['time', './sequence', '100', '4', '<', 'input-5.txt']
        result = subprocess.run(test_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=path)
        if result.returncode == 0:
            output = result.stdout.decode('utf-8').strip()
            # only get last 10 lines of output
            output = output.split('\n')[-10:]
            log("Test Case 6 (2)")
            log(output)
        else:
            log(f"Test Case 6 (2) Failed: {result.stderr.decode('utf-8')}")
        return score
    except Exception as e:
        print(f"Test Case 6 Error: {e}")
        log(f"Test Case 6 Error: {e}")
        return score

        
        
        
    

def grade_submission(submission_path):
    score: int = 0
    global path
    path = submission_path
    
    # Compile
    compile_result = compile()
    if not compile_result or compile_result.returncode != 0 :
        log("Compilation error")
        return score

    # Copy
    if (copy() is False):
        log("Error copying files")
        return score
    
    # TestCases
    score += test1()
    score += test2()
    score += test3()
    score += test4()
    score += test5()
    
