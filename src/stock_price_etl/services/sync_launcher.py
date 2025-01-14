import multiprocessing as mp

def sync_launcher(function, args_list):
    
    if isinstance(args_list[0], tuple):
        with mp.Pool(processes=mp.cpu_count()) as pool:
            pool.starmap(function, args_list)
    else:
        with mp.Pool(processes=mp.cpu_count()) as pool:
            pool.map(function, args_list)
