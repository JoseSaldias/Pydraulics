# Detalle de códigos

## ~/Columna rígida/vaciamiento estanque.py

Las ecuaciones de columna rígida corresponde a una simplificación del modelo elástico, endonde la velocidad de la onda mecánica es mucho mayor a la velocidad del fluido.

### Ecuación de continuidad:
<p align="center">
<a href="https://www.codecogs.com/eqnedit.php?latex=\frac{\partial&space;Q}{\partial&space;x}&space;=&space;0&space;\label{Continuidad}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\frac{\partial&space;Q}{\partial&space;x}&space;=&space;0&space;\label{Continuidad}" title="\frac{\partial Q}{\partial x} = 0 \label{Continuidad}" /></a>
</p>

### Consevación de cantidad de movimiento 
<p align="center">
<a href="https://www.codecogs.com/eqnedit.php?latex=\frac{\partial&space;Q}{\partial&space;t}&space;=&space;-gA\frac{\partial&space;H}{\partial&space;x}-&space;\frac{f\,&space;Q\,|Q|}{2DA}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\frac{\partial&space;Q}{\partial&space;t}&space;=&space;-gA\frac{\partial&space;H}{\partial&space;x}-&space;\frac{f\,&space;Q\,|Q|}{2DA}" title="\frac{\partial Q}{\partial t} = -gA\frac{\partial H}{\partial x}- \frac{f\, Q\,|Q|}{2DA}" /></a>
</p>

Uno de los problemas clásicos del método de columna rígida corresponde al vaciamiento de un estanque de  ́area transversal <img src="https://render.githubusercontent.com/render/math?math=A_e"> través de una tubería de diámetro <img src="https://render.githubusercontent.com/render/math?math=D">

Primero, mediante la ecuación de continuidad, establecemos de variaciones de volumen instantáneas en el sistema.

Luego,  la  ecuación  de  cantidad  de  movimiento  nos  da  una  relación  para  la  evolución  del caudal. Si tomamos que las cotas entre el estanque y la salida de la tubería la cota baja de <img src="https://render.githubusercontent.com/render/math?math=H_e"> a <img src="https://render.githubusercontent.com/render/math?math=0"> a lo largo de un largo <img src="https://render.githubusercontent.com/render/math?math=L">, entonces se cumple que

> <p align="center">
> <a href="https://www.codecogs.com/eqnedit.php?latex=\frac{\partial&space;H}{\partial&space;x}&space;=&space;-\frac{H}{L}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\frac{\partial&space;H}{\partial&space;x}&space;=&space;-\frac{H}{L}" title="\frac{\partial H}{\partial x} = -\frac{H}{L}" /></a>
> </p>

Con esto, la ecuación de conservación de cantidad de movimiento queda:

> <p align="center">
> <a href="https://www.codecogs.com/eqnedit.php?latex=\frac{\partial&space;Q}{\partial&space;t}&space;=&space;gA\frac{H}{L}&space;-&space;\frac{f\,&space;Q\,|Q|}{2DA}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\frac{\partial&space;Q}{\partial&space;t}&space;=&space;gA\frac{H}{L}&space;-&space;\frac{f\,&space;Q\,|Q|}{2DA}" title="\frac{\partial Q}{\partial t} = gA\frac{H}{L} - \frac{f\, Q\,|Q|}{2DA}" /></a>
> </p>

Con esto se compone un sistema de ecuaciones que se puede expresar de forma matricial:

> <p align="center">
> <a href="https://www.codecogs.com/eqnedit.php?latex=\frac{\partial}{\partial&space;t}&space;\begin{bmatrix}&space;H&space;\\&space;Q&space;\end{bmatrix}&space;=&space;\begin{bmatrix}&space;0&space;&&space;-\frac{1}{A_e}&space;\\&space;\frac{gA}{L}&space;&&space;0&space;\end{bmatrix}&space;\begin{bmatrix}&space;H&space;\\&space;Q&space;\end{bmatrix}&space;-&space;\begin{bmatrix}&space;0&space;\\&space;\frac{f\,&space;Q\,|Q|}{2DA}&space;\end{bmatrix}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\frac{\partial}{\partial&space;t}&space;\begin{bmatrix}&space;H&space;\\&space;Q&space;\end{bmatrix}&space;=&space;\begin{bmatrix}&space;0&space;&&space;-\frac{1}{A_e}&space;\\&space;\frac{gA}{L}&space;&&space;0&space;\end{bmatrix}&space;\begin{bmatrix}&space;H&space;\\&space;Q&space;\end{bmatrix}&space;-&space;\begin{bmatrix}&space;0&space;\\&space;\frac{f\,&space;Q\,|Q|}{2DA}&space;\end{bmatrix}" title="\frac{\partial}{\partial t} \begin{bmatrix} H \\ Q \end{bmatrix} = \begin{bmatrix} 0 & -\frac{1}{A_e} \\ \frac{gA}{L} & 0 \end{bmatrix} \begin{bmatrix} H \\ Q \end{bmatrix} - \begin{bmatrix} 0 \\ \frac{f\, Q\,|Q|}{2DA} \end{bmatrix}" /></a>
> </p>

Este sistema cumple la forma

> <p align="center">
> <a href="https://www.codecogs.com/eqnedit.php?latex=F(t,y)&space;=&space;\frac{dy}{dt}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?F(t,y)&space;=&space;\frac{dy}{dt}" title="F(t,y) = \frac{dy}{dt}" /></a>
> </p>

Entonces el valor de la variable <a href="https://www.codecogs.com/eqnedit.php?latex=y" target="_blank"><img src="https://latex.codecogs.com/gif.latex?y" title="y" /></a> puede ser resuelto a partir de una variación discreta <a href="https://www.codecogs.com/eqnedit.php?latex=\Delta&space;t" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\Delta&space;t" title="\Delta t" /></a> mediante el m ́etodo de Runge Kutta. Dada una discretización <a href="https://www.codecogs.com/eqnedit.php?latex=\Delta&space;t" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\Delta&space;t" title="\Delta t" /></a>, es posible estimar el valorde la función en el tiempo siguiente dado un cierto valor inicial <a href="https://www.codecogs.com/eqnedit.php?latex=y(t=t_0)=y_0" target="_blank"><img src="https://latex.codecogs.com/gif.latex?y(t=t_0)=y_0" title="y(t=t_0)=y_0" /></a> 

> <p align="center">
> <a href="https://www.codecogs.com/eqnedit.php?latex=y_{i&plus;1}=y_i&space;&plus;\frac{1}{6}&space;(k_1&space;&plus;2k_2&space;&plus;2k_3&space;&plus;k_4&space;)\Delta&space;t" target="_blank"><img src="https://latex.codecogs.com/gif.latex?y_{i&plus;1}=y_i&space;&plus;\frac{1}{6}&space;(k_1&space;&plus;2k_2&space;&plus;2k_3&space;&plus;k_4&space;)\Delta&space;t" title="y_{i+1}=y_i +\frac{1}{6} (k_1 +2k_2 +2k_3 +k_4 )\Delta t" /></a>
> </p>

Donde <a href="https://www.codecogs.com/eqnedit.php?latex=y_i" target="_blank"><img src="https://latex.codecogs.com/gif.latex?y_i" title="y_i" /></a> corresponde al valor de la variable <a href="https://www.codecogs.com/eqnedit.php?latex=y" target="_blank"><img src="https://latex.codecogs.com/gif.latex?y" title="y" /></a> en el tiempo <a href="https://www.codecogs.com/eqnedit.php?latex=i" target="_blank"><img src="https://latex.codecogs.com/gif.latex?i" title="i" /></a> donde la diferencia entre los instantes <a href="https://www.codecogs.com/eqnedit.php?latex=i" target="_blank"><img src="https://latex.codecogs.com/gif.latex?i" title="i" /></a> e <a href="https://www.codecogs.com/eqnedit.php?latex=i&plus;1" target="_blank"><img src="https://latex.codecogs.com/gif.latex?i&plus;1" title="i+1" /></a> es <a href="https://www.codecogs.com/eqnedit.php?latex=\Delta&space;t" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\Delta&space;t" title="\Delta t" /></a>. Luego, los valores de k están dados por interpolaciones que relacionanambos instantes, vinculadas a los datos conocidos.

> <p align="center">
> <a href="https://www.codecogs.com/eqnedit.php?latex=\\&space;\\&space;k_1&space;=&space;F(t_i,y_i)&space;\\&space;\\&space;k_2&space;=&space;F(t_i&space;&plus;\frac{1}{2}\Delta&space;t,&space;y_i&space;&plus;&space;\frac{1}{2}k_1&space;\Delta&space;t)&space;\\&space;\\&space;k_3&space;=&space;F(t_i&space;&plus;\frac{1}{2}\Delta&space;t,&space;y_i&space;&plus;&space;\frac{1}{2}k_2&space;\Delta&space;t)&space;\\&space;\\&space;k_4&space;=&space;F(t_i&plus;\Delta&space;t,&space;y_i&space;&plus;&space;k_3&space;\Delta&space;t)" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\\&space;\\&space;k_1&space;=&space;F(t_i,y_i)&space;\\&space;\\&space;k_2&space;=&space;F(t_i&space;&plus;\frac{1}{2}\Delta&space;t,&space;y_i&space;&plus;&space;\frac{1}{2}k_1&space;\Delta&space;t)&space;\\&space;\\&space;k_3&space;=&space;F(t_i&space;&plus;\frac{1}{2}\Delta&space;t,&space;y_i&space;&plus;&space;\frac{1}{2}k_2&space;\Delta&space;t)&space;\\&space;\\&space;k_4&space;=&space;F(t_i&plus;\Delta&space;t,&space;y_i&space;&plus;&space;k_3&space;\Delta&space;t)" title="\\ \\ k_1 = F(t_i,y_i) \\ \\ k_2 = F(t_i +\frac{1}{2}\Delta t, y_i + \frac{1}{2}k_1 \Delta t) \\ \\ k_3 = F(t_i +\frac{1}{2}\Delta t, y_i + \frac{1}{2}k_2 \Delta t) \\ \\ k_4 = F(t_i+\Delta t, y_i + k_3 \Delta t)" /></a>
> </p>

A modo de ejemplo, se muestran los cálculos para un paso de tiempo en el sistema de columna rígida.

> <p align="center">
> <a href="https://www.codecogs.com/eqnedit.php?latex=\\&space;\\&space;{k_1^{H}}=-\frac{Q_i}{A_e}&space;\\&space;\\&space;{k_1^{Q}}=ga\frac{H_i}{L}&space;-&space;\frac{f\,&space;Q_i\,|Q_i|}{2DA}&space;\\&space;\\&space;{k_2^{H}}=-\frac{Q_i&space;&plus;k_1^{Q}\frac{\Delta&space;t}{2}&space;}{A_e}&space;\\&space;\\&space;{k_2^{Q}}&space;=&space;ga\frac{(H_i&plus;k_1^{H}\frac{\Delta&space;t}{2})}{L}&space;-&space;\frac{f\,&space;(Q_i&plus;k_1^{Q}\frac{\Delta&space;t}{2})\,(|Q_i&plus;k_1^{Q}\frac{\Delta&space;t}{2}|)}{2DA}&space;\\&space;\\&space;{k_3^{H}}=-\frac{Q_i&space;&plus;k_2^{Q}\frac{\Delta&space;t}{2}&space;}{A_e}&space;\\&space;\\&space;{k_3^{Q}}&space;=&space;ga\frac{(H_i&plus;k_2^{H}\frac{\Delta&space;t}{2})}{L}&space;-&space;\frac{f\,&space;(Q_i&plus;k_2^{Q}\frac{\Delta&space;t}{2})\,(|Q_i&plus;k_2^{Q}\frac{\Delta&space;t}{2}|)}{2DA}&space;\\&space;\\&space;{k_4^{H}}=-\frac{Q_i&space;&plus;k_3^{Q}\Delta&space;t}{A_e}&space;\\&space;\\&space;{k_4^{Q}}&space;=&space;ga\frac{(H_i&plus;k_3^{H}\Delta&space;t)}{L}&space;-&space;\frac{f\,&space;(Q_i&plus;k_2^{Q}\Delta&space;t)\,(|Q_i&plus;k_2^{Q}\Delta&space;t|)}{2DA}&space;\\&space;\\&space;H_{i&plus;1}=&space;H_i&space;&plus;\frac{1}{6}&space;(k_1^{H}&space;&plus;2k_2^{H}&space;&plus;2k_3^{H}&space;&plus;k_4^{H}&space;)\Delta&space;t&space;\\&space;\\&space;Q_{i&plus;1}=&space;Q_i&space;&plus;\frac{1}{6}&space;(k_1^{Q}&space;&plus;2k_2^{Q}&space;&plus;2k_3^{Q}&space;&plus;k_4^{Q}&space;)\Delta&space;t" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\\&space;\\&space;{k_1^{H}}=-\frac{Q_i}{A_e}&space;\\&space;\\&space;{k_1^{Q}}=ga\frac{H_i}{L}&space;-&space;\frac{f\,&space;Q_i\,|Q_i|}{2DA}&space;\\&space;\\&space;{k_2^{H}}=-\frac{Q_i&space;&plus;k_1^{Q}\frac{\Delta&space;t}{2}&space;}{A_e}&space;\\&space;\\&space;{k_2^{Q}}&space;=&space;ga\frac{(H_i&plus;k_1^{H}\frac{\Delta&space;t}{2})}{L}&space;-&space;\frac{f\,&space;(Q_i&plus;k_1^{Q}\frac{\Delta&space;t}{2})\,(|Q_i&plus;k_1^{Q}\frac{\Delta&space;t}{2}|)}{2DA}&space;\\&space;\\&space;{k_3^{H}}=-\frac{Q_i&space;&plus;k_2^{Q}\frac{\Delta&space;t}{2}&space;}{A_e}&space;\\&space;\\&space;{k_3^{Q}}&space;=&space;ga\frac{(H_i&plus;k_2^{H}\frac{\Delta&space;t}{2})}{L}&space;-&space;\frac{f\,&space;(Q_i&plus;k_2^{Q}\frac{\Delta&space;t}{2})\,(|Q_i&plus;k_2^{Q}\frac{\Delta&space;t}{2}|)}{2DA}&space;\\&space;\\&space;{k_4^{H}}=-\frac{Q_i&space;&plus;k_3^{Q}\Delta&space;t}{A_e}&space;\\&space;\\&space;{k_4^{Q}}&space;=&space;ga\frac{(H_i&plus;k_3^{H}\Delta&space;t)}{L}&space;-&space;\frac{f\,&space;(Q_i&plus;k_2^{Q}\Delta&space;t)\,(|Q_i&plus;k_2^{Q}\Delta&space;t|)}{2DA}&space;\\&space;\\&space;H_{i&plus;1}=&space;H_i&space;&plus;\frac{1}{6}&space;(k_1^{H}&space;&plus;2k_2^{H}&space;&plus;2k_3^{H}&space;&plus;k_4^{H}&space;)\Delta&space;t&space;\\&space;\\&space;Q_{i&plus;1}=&space;Q_i&space;&plus;\frac{1}{6}&space;(k_1^{Q}&space;&plus;2k_2^{Q}&space;&plus;2k_3^{Q}&space;&plus;k_4^{Q}&space;)\Delta&space;t" title="\\ \\ {k_1^{H}}=-\frac{Q_i}{A_e} \\ \\ {k_1^{Q}}=ga\frac{H_i}{L} - \frac{f\, Q_i\,|Q_i|}{2DA} \\ \\ {k_2^{H}}=-\frac{Q_i +k_1^{Q}\frac{\Delta t}{2} }{A_e} \\ \\ {k_2^{Q}} = ga\frac{(H_i+k_1^{H}\frac{\Delta t}{2})}{L} - \frac{f\, (Q_i+k_1^{Q}\frac{\Delta t}{2})\,(|Q_i+k_1^{Q}\frac{\Delta t}{2}|)}{2DA} \\ \\ {k_3^{H}}=-\frac{Q_i +k_2^{Q}\frac{\Delta t}{2} }{A_e} \\ \\ {k_3^{Q}} = ga\frac{(H_i+k_2^{H}\frac{\Delta t}{2})}{L} - \frac{f\, (Q_i+k_2^{Q}\frac{\Delta t}{2})\,(|Q_i+k_2^{Q}\frac{\Delta t}{2}|)}{2DA} \\ \\ {k_4^{H}}=-\frac{Q_i +k_3^{Q}\Delta t}{A_e} \\ \\ {k_4^{Q}} = ga\frac{(H_i+k_3^{H}\Delta t)}{L} - \frac{f\, (Q_i+k_2^{Q}\Delta t)\,(|Q_i+k_2^{Q}\Delta t|)}{2DA} \\ \\ H_{i+1}= H_i +\frac{1}{6} (k_1^{H} +2k_2^{H} +2k_3^{H} +k_4^{H} )\Delta t \\ \\ Q_{i+1}= Q_i +\frac{1}{6} (k_1^{Q} +2k_2^{Q} +2k_3^{Q} +k_4^{Q} )\Delta t" /></a>
> </p>

### Ejemplo de utilización

<p align="center">
  <a href="https://ibb.co/4Wy1gb2"><img src="https://i.ibb.co/2q2ZYzS/Ejemplo.png" alt="Ejemplo" border="0"></a>
</p>
