from imagekitio import ImageKit
from imagekitio.models.UploadFileRequestOptions import UploadFileRequestOptions

class imagekit_image_upload:

    imagekit = ImageKit(
        private_key='private_g8H2q8vGkKAvKC6QsJeNSR4ccqY=',
        public_key='public_zfGdEDeWI+7ln4MsrkaJzfZVhfI=',
        url_endpoint='https://ik.imagekit.io/1lrfahap7'
    )

    # return url from object
    def upload_image_and_get_url(self, img_url, platform):

        #options
        options = UploadFileRequestOptions(
            use_unique_file_name=False,
            folder=f'/{platform}/',
            is_private_file=False,
            overwrite_file=True
        )

        image_name = img_url.split('/')[-1]
        upload = self.imagekit.upload(
            file=img_url,  # image url here
            file_name=image_name,
            options=options
        )
        #print(upload.response_metadata.raw)
        return upload.file_id, upload.name, upload.url, upload.thumbnail_url


# i = imagekit_image_upload()

# a1,a2,a3=i.upload_image_and_get_url('https://m.media-amazon.com/images/I/61S9aVnRZDL._SX679_.jpg',"amazon")
