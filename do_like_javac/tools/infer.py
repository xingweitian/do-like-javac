import os
import argparse
import common

argparser = argparse.ArgumentParser(add_help=False)
infer_group = argparser.add_argument_group('inference tool arguments')

infer_group.add_argument('-s', '--solver', metavar='<solver>',
                        action='store',default='checkers.inference.solver.DebugSolver',
                        help='solver to use on constraints')
infer_group.add_argument('-afud', '--afuOutputDir', metavar='<afud>',
                        action='store',default='afud/',
                        help='Annotation File Utilities output directory')
infer_group.add_argument('-m', '--mode', metavar='<mode>',
                        action='store',default='INFER',
                        help='Modes of operation: TYPECHECK, INFER, ROUNDTRIP,ROUNDTRIP_TYPECHECK')
infer_group.add_argument('-solverArgs', '--solverArgs', metavar='<solverArgs>',
                        action='store',default='backEndType=maxsatbackend.MaxSat',
                        help='arguments for solver')
infer_group.add_argument('-cfArgs', '--cfArgs', metavar='<cfArgs>',
                        action='store',default='',
                        help='arguments for checker framework')
infer_group.add_argument('-j', '--jar', metavar='<a.jar b.jar c.jar ...>',
                        action='store', dest='jarFileList', nargs='*',
                        help='List of the name of jar files that checker framework inference needs.')

def run(args, javac_commands, jars):
    # the dist directory if CFI.
    CFI_dist = os.path.join(os.path.abspath(os.path.join(os.getcwd(), "../../../")), 'checker-framework-inference', 'dist')
    CFI_command = ['java']

    print os.environ

    for jc in javac_commands:
        target_cp = jc['javac_switches']['classpath'] + \
            ':'.join([os.path.join(args.lib_dir, each_jar) for each_jar in args.jarFileList])

        cp = target_cp + \
             ':' + os.path.join(CFI_dist, 'checker.jar') + \
             ':' + os.path.join(CFI_dist, 'plume.jar') + \
             ':' + os.path.join(CFI_dist, 'com.microsoft.z3.jar') + \
             ':' + os.path.join(CFI_dist, 'checker-framework-inference.jar')

        if 'CLASSPATH' in os.environ:
            cp += ':' + os.environ['CLASSPATH']

        cmd = CFI_command + ['-classpath', cp,
                             'checkers.inference.InferenceLauncher',
                             '--solverArgs', args.solverArgs,
                             '--cfArgs', args.cfArgs,
                             '--checker', args.checker,
                             '--solver', args.solver,
                             '--mode', args.mode,
                             '--hacks=true',
                             '--targetclasspath', target_cp,
                             '--logLevel=WARNING',
                             '-afud', args.afuOutputDir]
        cmd.extend(jc['java_files'])

        common.run_cmd(cmd, args, 'infer')
