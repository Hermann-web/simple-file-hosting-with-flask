/*
<div class="wrapper">
    <div class="progress-bar">
        <span class="progress-bar-fill"></span>  
    </div>
    <span class="progress-text">Download starting...</span>
</div>
*/

const download_wrapper_id = "download-wrapper";
const download_link_id = "download-btn";

function add_bar_into_download_wrapper(){
    // Create a new div with the class and content you want to add
    var newContent = document.createElement('div');
    newContent.setAttribute('class', 'wrapper');
    newContent.innerHTML = `
        <div class="progress-bar">
            <span class="progress-bar-fill"></span>  
        </div>
        <span class="progress-text">Download starting...</span>
    `;

    // Get the download-wrapper element
    var downloadWrapper = document.getElementById(download_wrapper_id);

    // Append the new content to the download-wrapper
    if (downloadWrapper) {
        downloadWrapper.appendChild(newContent);
    }
}


document.addEventListener('DOMContentLoaded', () => {

    add_bar_into_download_wrapper()

    // Initially hide the download wrapper
    var downloadWrapper = document.getElementById(download_wrapper_id);
    downloadWrapper.style.display = 'none';


    const downloadLink = document.getElementById(download_link_id);

    downloadLink.addEventListener('click', (event) => {
        event.preventDefault(); // Prevent the default behavior of the link

        downloadWrapper.style.display = 'block';

        const fill = document.querySelector('.progress-bar-fill');
        const text = document.querySelector('.progress-text');

        fetch(downloadLink.href) // Fetch the download link URL
        .then(response => {
            const contentLength = response.headers.get('content-length');
            let loaded = 0;

            return new Response(
            new ReadableStream({
                start(controller) {
                const reader = response.body.getReader();
                read();
                function read() {
                    reader.read()
                    .then((progressEvent) => {
                        if (progressEvent.done) {
                        controller.close();
                        return;
                        }

                        let updateProgressAndContinue = ()=>{
                            loaded += progressEvent.value.byteLength;

                            const percentageComplete = Math.round(loaded / contentLength * 100) + '%';
                            fill.style.width = percentageComplete;
                            text.innerText = percentageComplete;

                            controller.enqueue(progressEvent.value);
                            read();
                        }

                        updateProgressAndContinue();
                        // setTimeout(updateProgressAndContinue, 10000);
                        
                    })
                }
                }
            })
            );
        })
        .then(response => response.blob())
        .then(blob => {
            // Create a temporary link to trigger the download
            const tempLink = document.createElement('a');
            tempLink.href = URL.createObjectURL(blob);

            // Extract filename from the URL
            const url = downloadLink.href;
            const filename = url.substring(url.lastIndexOf('/') + 1);

            tempLink.setAttribute('download', filename || 'downloaded_file'); // Set the filename

            tempLink.style.display = 'none';
            document.body.appendChild(tempLink);
            tempLink.click();
            document.body.removeChild(tempLink);
            // downloadWrapper.style.display = 'none';
        })
        .catch(error => {
            // Handle any errors that occur during the fetch
            console.error('Download failed:', error);
        });
    });
});
