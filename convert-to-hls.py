import click
import logging
import ffmpeg

@click.command()
@click.option("--test", "-t", default = 1, help = "Test Value")
@click.option("--infile", "-i", default = 'out.mp4', help = "mp4 video file inputted by the user")
@click.option("--outfile", "-o", default = 'output.m3u8',  help = "Name of the export file")

def main(test, infile, outfile):
    #for file conversion
    media_input_filename = infile
    playlist_filename = outfile
    input_stream = ffmpeg.input(media_input_filename, f='mp4')
    output_stream = ffmpeg.output(input_stream, playlist_filename, format='hls', start_number=0, hls_time=5, hls_list_size=0)
    ffmpeg.run(output_stream)
    click.echo("Files: " + media_input_filename + " and " + playlist_filename)
    testVariable(test)

def testVariable(test_var):
    #for test variables
    print(f"My local test variable is: {test_var}")


if __name__ == "__main__":
    """
    This initiates and calls the main function for this application. 

    Generally, this should be the last bit of code in this script.
    """
    logging.basicConfig(level=logging.DEBUG)
    main()
