Docker image
------------

Build: 
```bash
cd docker && docker build -t deeppomf/DeepCreamPy:latest . 
```

Run:
```bash
docker run -v <input_path>:/opt/DeepCreamPy/decensor_input -v <output_path>:/opt/DeepCreamPy/decensor_output deeppomf/DeepCreamPy:latest
```
where
<input_path> - full path to input directory
<output_path> - full path to output directory