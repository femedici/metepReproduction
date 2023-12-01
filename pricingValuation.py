import numpy as np
import scipy.optimize as optimize
import matplotlib.pyplot as plt

def cost_plus(costs, stock=0):
    total_costs = costs
    stock = stock
    price = total_costs + (0.4 * total_costs)
    p_0 = (total_costs / (100 - 50)) * 100

    for x in range(1, stock + 1):
        sales = price * x
        s_0 = p_0 * x
        pro_0 = s_0 - (total_costs * x)
        profit = sales - (total_costs * x)

        print('Sale: %d  Sales: %d Profit: %d' % (x, sales, profit))

    return price

def price(x, a=200, b=10, d=10, t=np.linspace(1, 10, 10)):
    return (a - b * x) * d / (d + t)

# Gera valores aleatórios de preços para serem tratados depois pelas funções de precificação
def price_values(p, num_prices=10):
    p_vals = []
    for x in range(1, num_prices + 1):
        p = p - (0.033 * p * x)
        p[p < 0] = 0  
        p_vals.append(p.copy())
        
    return p_vals

# Diferentes tipos de funções para otimização de preço em relação ao tempo

    # Estibulação das variaveis de decisão (x_t) são no caso um otimizador das funções para maximiar ou minimizar aquela função
    # ou seja, faz o papel determinar o grau de dificuldade daquela issue para jogar o preço mais acima ou mais abaixo caso o grau seja menor

def demand(p, a=200, b=10, d=10, t=np.linspace(1, 10, 10)):
    return 1.0 / b * (a - p * (d + t) / d)

def objective(x_t, a=512, b=10, d=10, t=np.linspace(1, 10, 10)):
    return -1.0 * np.sum(x_t * price(x_t, a=a, b=b, d=d, t=t))

def constraint_1(x_t, s_0=150):
    return s_0 - np.sum(x_t)

def constraint_2(x_t):
    return x_t

def constraint_3(x_t, a=200, b=10):
    return (a / b) - x_t

def dynamic_pricing(time=0, stock=0):
    s_0 = stock
    a = 1650
    b = 10.0
    d = 10.0
    t = np.linspace(1, 20, 20)

    x_start = 3.0 * np.ones(len(t))
    bounds = tuple((0, 20.0) for x in x_start)

    constraints = [
        {'type': 'ineq', 'fun': lambda x, s_0=s_0: constraint_1(x, s_0=s_0)},
        {'type': 'ineq', 'fun': lambda x: constraint_2(x)},
        {'type': 'ineq', 'fun': lambda x, a=a, b=b: constraint_3(x, a=a, b=b)}
    ]

    opt_results = optimize.minimize(objective, x_start, args=(a, b, d, t),
                                    method='SLSQP', bounds=bounds, constraints=constraints)

    print("Optimization Results:")
    print(opt_results)

    # Exibindo gráfico com os resultados
    plt.figure(figsize=(12, 8))

    plt.subplot(2, 1, 1)
    plt.plot(t, opt_results.x, 'bo-')
    plt.title('Variáveis de Decisão Otimizadas')
    plt.xlabel('Tempo')
    plt.ylabel('Variável de Decisão')

    plt.subplot(2, 1, 2)
    prices = price_values(opt_results.x, num_prices=10)
    for i, p in enumerate(prices):
        plt.plot(t, price(p, a=a, b=b, d=d, t=t) * (i + 1), label=f'Price {i + 1}')

    plt.title('10 Tipos Diferentes de Preços Otimizados ao Longo do Tempo')
    plt.xlabel('Tempo')
    plt.ylabel('Preço')
    plt.legend()

    plt.tight_layout()
    plt.show()

# Chamada da função dynamic_pricing 
# onde vai ser feito todo o tratamento das operações e precificações
dynamic_pricing(time=0, stock=20)
