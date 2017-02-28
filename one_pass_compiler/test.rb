#!/usr/bin/ruby

module Execute
  def execute( cmd )
    puts "#{cmd}"
    res = `#{cmd}`
    return res
  end
end

class Tester
  include Execute
  def initialize( args )
    get_test_dir

    files = check_file_arg( args[0] )
    check_gcc_arg( args[1] )

    @report = "gcc_test_results.txt"
    execute("\\rm -f #{@report}") if File.file?(@report)

    @tests = Array.new

    files.each{ |f|
      @tests << Test.new( @test_dir, f, @gcc, @report )
    }
  end

  def test
    @tests.each{ |t| t.test }
    puts "Testing finished.  The results are in #{Dir.getwd}/#{@report}.\n\n"
  end

  def get_root_dir
    found = false
    file = '.hg'
    while not File.exist?(file) and File.directory?(File.dirname(file))
      file = '../' + file
    end
    if not File.exist?( file ) 
      abort("Abort: can't find the hg repository root in parent directories")
    end
    return File.dirname(File.expand_path( file ) )
  end

  def get_test_dir
    root = get_root_dir
    @test_dir = "#{root}/assignments/hwk04/test_files"
  end

  def check_file_arg( arg )
    all = Dir.new(@test_dir).entries()
    all.delete(".")
    all.delete("..")
    return all if ( arg.downcase == 'all' )
    
    file = File.basename(arg, ".c")
    if not File.exists?( "#{@test_dir}/#{file}.c")
      abort("Test program #{file}.c not found.  Choose one of the following: #{all * ', '}")
    end
    return ["#{file}.c"]
  end

  def check_gcc_arg( arg )
    abort( "#{arg} does not exist (or it is not an executable)" ) if not (File.exists?(arg) and File.executable?(arg))
    @gcc = arg
  end
end

class Test
  include Execute

  def initialize( dir, prog, gcc, report )
    @dir, @prog, @gcc, @report = dir, prog, gcc, report
    @params = Hash.new
    @params[ "automaton.c" ] = "1 0 0 1 0 0 -1"
    @params[ "binrep.c" ] = "255"
    @params[ "movingedge.c" ] = "455 42"
    @params[ "multiply.c" ] = "1000 50"
    @params[ "tax.c" ] = "20000 200 20 0 1 2100 0"
    @params[ "trivia.c" ] = "20"
    @params[ "MeaningOfLife.c" ] = 100
  end

  def test
    puts "testing #{@prog} ..."
    tmp = "tmp_#{@prog}"
    execute("echo \"#include <stdio.h>\n\" > #{tmp}")
    execute("cat #{@dir}/#{@prog} >> #{tmp}")
    execute("#{@gcc} #{tmp}")
    execute("echo \"CS254 Test (#{Time.now}): #{@prog}\" >> #{@report}")
    if @params[ @prog ] != nil
      execute("echo \"#{@params[@prog]}\" | ./a.out >> #{@report}")
    else
      execute("./a.out >> #{@report}")
    end
    File.delete("a.out")
    File.delete(tmp)
  end
end

if ARGV.size != 2
  abort("\tUsage: test.rb [all | prog_name ] your_gcc\n\tExplanations: 'prog_name' is a test in projects/test_cases. Use 'all' to test all .c files in the directory with standard inputs.")  
# You will be asked whether to submit the results.  New results may be submitted to replce the previous submission.")
end

tester = Tester.new( ARGV )
tester.test
