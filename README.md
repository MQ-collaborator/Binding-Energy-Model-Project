# Binding Energy Model Project
 This project is a computation of the coefficients of the nuclear binding energy formula proposed in the semi-emperical-mass-formula for binding energy. The coefficients were found using gradient descent and the 4000 experiemntally measured binding energies of nuclei as training data. 
Below is detailed documentation of the problem solved and methodology used:

# Problem
## Explaining Binding Energy
For all atomic nuclei, the mass of the nucleus is less than the mass of the separated nucleons within the nucleus. This difference in mass is known as the mass defect.
![MassDefect](https://github.com/user-attachments/assets/a7aa397b-d47c-4991-891d-70108a3eeb84)
However, we can equate this mass to an energy using Einstein’s mass-energy equivalence:

$$E=mc^2$$

The energy equivalent to the **mass defect** is known as **binding energy.**

The **binding energy** for all nuclei has been found experimentally. There is no closed for solution for this problem. The binding energy data for this project can be [found online](https://www.nndc.bnl.gov/nudat3/). 

One of the more accurate ways of predicting binding energies is the [semi-empirical mass formula](https://en.wikipedia.org/wiki/Semi-empirical_mass_formula)

## Formula
The most prevalent formula for predicting binding energies using the semi-empirical mass formula is:
![BEformula](https://github.com/user-attachments/assets/dbde0264-aaed-4ccf-b4b0-89e9292d1534)

Where:
- B = Binding energy in MeV
- A = Atomic mass
- Z = Atomic Number
The coefficients of the formula above (a_v, a_s, a_c, a_a, a_p) must be calculated using experimental data.

**The goal of my project is to calculate these coefficients computationally using the 4000 known binding energies for nuclei documented online.** There exist several different calculations of these coefficients (as seen in the Wikipedia article) for two reasons:

- It is impossible to find a set of coefficients that produces a global minimum in the **Loss function** (a measure of how close our model is to real life values which will be discussed later).
- There is uncertainty in binding energy data and different sources often quote slightly different data. For small nuclei this uncertainty is significant.
- The local minimum obtained is sensitive to the accuracy of the numerical methods used and the arbitrary starting values of coefficients set (before optimization).

That being said, all calculations for these coefficients online fall within roughly +-10% of the values below:
![SampleValues](https://github.com/user-attachments/assets/2d17a424-8311-4bf9-b65f-5a591c9197ba)

My results (methodology discussed later) also falls within this range. 
# Methodolgy 
The goal when calculating these coefficients is to minimize the average distance between our expected values for binding energy and calculated values
## Loss Function

$$ L = \sum_{i=0}^n (B_i - E_i)^2 $$

Where:

- L is the loss function
- n is number of nuclei for which we have binding energy data
- $B_i$ is the calculated binding energy for the ith nucleus using the model mentioned before and the current values of the coefficients a_v to a_p
- $E_i$  is the expected value of binding energy (from experiment).

The Loss function is thus a measure of how close our model is to actual values (the sum of the squares of distance). This is easily understood with the linear example below:
![LinearRegression](https://github.com/user-attachments/assets/67c5ce4d-bd37-43db-b1d1-b1c4501fdd0a)

Many models divide the loss function by the number of datapoints to find the average distance between model and datapoints.

## Gradient descent - minimizing loss function

Our goal is to adjust the coefficients (parameters) of the loss function to minimize the loss function. To do this we perform gradient descent:
![GradientDescent1](https://github.com/user-attachments/assets/ee759fcc-6384-4e82-ad31-0376876edf13)
![GradeintDescent2](https://github.com/user-attachments/assets/e428a64b-ec61-4625-9af8-eaee16d9f650)

To do this, we calculate the partial derivative of the loss function with respect to our parameters(s). We then subtract the gradient multiplied by our learning rate from the value of the parameter (moving in the direction opposite to the gradient should move us toward a local minimum). We then repeat this with the new value of the parameter until a local minimum is reached.

3D visualization:

![GradientDescent3D](https://github.com/user-attachments/assets/86f4d16c-6884-4d86-a357-568573d74bf1)

Here a local minimum is the low point of a valley.

Our model has 5 parameters. 6D model is impossible. The five coefficients (parameters) were turned into a vector so that we could calculate grad of the loss function and subtract it from our vector **V.**

Formula for gradient descent:

$$ V_{n+1} = V_n - \mu \nabla L(V) $$

Where $\mu$ is our learning rate. A large value of  $\mu$ allows us to find local minimum quickly but we might overshoot it. A small value of  $\mu$ is slow (more computations required) but more accurate. 

### Numerical differentiation

To calculate the gradient of L for a given vector V we employ automatic differentiation. To do so, we repeat the process below for each of our five parameters:

---

- Calculate the value of $L(V_1)$ where $V_1$ the current value of **V** vector.
- Increment the parameter in question by 0.01 (width of tangent line, arbitrary small number)
- Calculate the value of $L(V_2)$ where $V_2$ is vector **V** with one parameter incremented..

If the parameter with which we are differentiating is $a_i$ then:

$$
\frac{\partial L}{\partial a_i} = \frac{(L(V_2)-L(V_1))}{0.01}
$$

---

This method is based on differentiation from first principles. 

It has the following benefits and shortcomings:

- Floating point imprecision - there is a limit to how accurately we can perform computations with floating point numbers (real numbers) because we have a limited number of decimal places (finite memory).
- Quick and simple to implement.
- We have implemented only the forward derivative here.
    - Using a value just above and just below the current value of parameter is more accurate but makes our program slower: currently we only calculate $L(V_1)$ once.

Numerical differentiation provides the derivatives needed for gradient descent.
The only viable alternative is automatic differentiation.

# Results
I obtained the following results (all in MeV)

- a_v=14.57815846
- a_s=17.48660865
- a_c=0.86090651
- a_a=23.33699972
- a_p=11.00090443
The starting values were set in the region near the results of other experiments to accelerate learning because at the time of running this project, the computing power available to me is limited.
The model programmed here can take a long or short time depending on the gradient value at which we stop gradient descent.  

Starting conditions:

- a_v=15.5
- a_s=17.3
- a_c=0.68
- a_a=23.3
- a_p=11

The data I obtained is very close to other values in literature, suggesting that the model is good. The most clear possible alterations are using a smaller learning rate, lowering the threshold of gradient considered to be 0 or calculating derivative more accurately (smaller tangent width or **automatic differentiation**).

These results produced a model which predicted binding energy with high accuracy for most nuclei. Exceptions are nuclei under 20 nucleons, for which the average error was higher.










