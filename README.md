libreoffice Microservice
========================

Alpine container service for [libreoffice](https://libreoffice.org/).

## Usage

Run Container
```bash
docker run -d -p 29881:80 agilize/libreoffice
curl -X POST -vv -F 'file=@demo.docx' http://localhost:29881 -o demo.pdf
```

You can found all libreoffice option here: [https://help.libreoffice.org/Common/Starting_the_Software_With_Parameters](https://help.libreoffice.org/Common/Starting_the_Software_With_Parameters)

### PHP example

```php
<?php

$demoPath = realpath('./demo.docx');

$libreofficeOptions = [
];

// set request body
$data = [
    'file' => curl_file_create($demoPath),
    'options' => json_encode($libreofficeOptions)
];

// set header
$headers = [
];

// curl options
$options = [
    CURLOPT_URL            => 'http://localhost/',
    CURLOPT_PORT           => 29881,
    CURLOPT_POST           => 1,
    CURLOPT_POSTFIELDS     => $data,
    CURLOPT_HTTPHEADER     => $headers,
    CURLOPT_RETURNTRANSFER => true
];

// curl call
$ch = curl_init();
curl_setopt_array($ch, $options);
$result = curl_exec($ch);
curl_close($ch);

// print result
echo $result;
```